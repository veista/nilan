"""CTS700 Nordic optional controls, fan percent mapping, and heat-source activity.

Separated from device_cts700_nordic.py to keep modules under the 500-line cap.
"""

from __future__ import annotations

import logging

from .registers import CTS700NordicRegisters as Reg

_LOGGER = logging.getLogger(__name__)

# Supply fan percent targets for steps 1-4 (holdings 20140/42/44/46).
_FAN_STEP_SUPPLY_REGS = (
    Reg.fan_speed_level_1_supply,
    Reg.fan_speed_level_2_supply,
    Reg.fan_speed_level_3_supply,
    Reg.fan_speed_level_4_supply,
)
_FAN_STEP_DEFAULT_PERCENTS = (45, 55, 75, 100)


class CTS700NordicControlsMixin:
    """Mixin: pauses, cooling/humidity/frost/legionella, fan %, heat activity."""

    async def _fan_step_percent_table(self) -> list[tuple[int, int]]:
        """Return [(step, percent), ...] from live 2014x or defaults."""
        table: list[tuple[int, int]] = []
        for step, address in enumerate(_FAN_STEP_SUPPLY_REGS, start=1):
            value = await self._read_holding_unsigned(address)
            if value is not None and 0 <= value <= 100:
                table.append((step, value))
        if len(table) == 4:
            return table
        return list(enumerate(_FAN_STEP_DEFAULT_PERCENTS, start=1))

    async def _percent_to_fan_step(self, percent: int) -> int:
        """Nearest fan step for a 0-100 percent reading on 4747 / 21771."""
        table = await self._fan_step_percent_table()
        best_step, _ = min(table, key=lambda item: abs(item[1] - percent))
        return best_step

    async def _fan_step_to_percent(self, step: int) -> int:
        """Percent target for fan step 1-4."""
        table = dict(await self._fan_step_percent_table())
        return int(table.get(step, _FAN_STEP_DEFAULT_PERCENTS[step - 1]))

    async def get_ventilation_step(self) -> int | None:
        """Fan step 1-4 from holding 4747 (101-104) or percent (0-100).

        Some Compact P Nordic firmwares hold percent on 4747 (same as 21771)
        instead of classic 101-104. Map percent via nearest step table.
        """
        value = await self._read_holding_unsigned(Reg.user_fan_step)
        if value is None:
            # Fall back to fan power percent readout
            value = await self._read_holding_unsigned(Reg.fan_power_percent)
        if value is None:
            _LOGGER.error("Could not read get_ventilation_step")
            return None
        if 101 <= value <= 104:
            return value - 100
        if value in (1, 2, 3, 4):
            return value
        if 0 <= value <= 100:
            return await self._percent_to_fan_step(value)
        return 1

    async def set_ventilation_step(self, mode: int) -> bool:
        """Write fan step as 101-104, or as step percent when 4747 is percent."""
        if mode not in (1, 2, 3, 4):
            _LOGGER.debug("Ignoring Nordic fan step %s (valid 1-4)", mode)
            return False
        current = await self._read_holding_unsigned(Reg.user_fan_step)
        if current is not None and 0 <= current <= 100 and current < 101:
            percent = await self._fan_step_to_percent(mode)
            return await self._write_holding(Reg.user_fan_step, percent)
        if current is not None and 101 <= current <= 104:
            return await self._write_holding(Reg.user_fan_step, 100 + mode)
        # Unknown encoding: try classic step first, then percent
        if await self._write_holding(Reg.user_fan_step, 100 + mode):
            verify = await self._read_holding_unsigned(Reg.user_fan_step)
            if verify is not None and (
                verify == 100 + mode or verify in (1, 2, 3, 4)
            ):
                return True
        percent = await self._fan_step_to_percent(mode)
        return await self._write_holding(Reg.user_fan_step, percent)

    async def get_actively_heating(self) -> bool | None:
        """True only when room heat is actually running.

        Holding 5432 can stay in heat for many hours while compressor effort
        (4706) cycles through 0 during thermostat hysteresis. Smart-plug
        correlation on Compact P: idle about 40 W, active heat about 500-700 W.
        Do not treat mode=heat alone as hvac_action=heating.
        DHW (5432=4) and cool (5432=1) compressor work is not room heating.
        """
        raw = await self._raw_operation_mode()
        if raw in (1, 4):
            return False
        effort = await self.get_main_compressor_effort()
        heater = await self._read_holding_unsigned(Reg.heater_control)
        if effort is None and heater is None:
            return None
        if effort is not None and effort > 0:
            return True
        if heater is not None and heater > 0:
            return True
        return False

    async def get_actively_cooling(self) -> bool | None:
        """True when compressor effort shows active cooling work."""
        raw = await self._raw_operation_mode()
        if raw is None:
            return None
        if raw != 1:
            return False
        effort = await self.get_main_compressor_effort()
        if effort is None:
            return None
        return effort > 0

    async def get_panel_operating_mode(self) -> int | None:
        """Raw holding 5432: panel Hot water production / Heating / Cooling.

        Values (community + Compact P Nordic map): 0 off, 1 cool, 2 heat,
        3 dehum, 4 DHW. Always reports the controller mode, including during
        thermostat hysteresis when compressor effort 4706 is 0.
        """
        return await self._raw_operation_mode()

    async def get_control_state(self) -> int | None:
        """Approximate control state for climate action UI from raw 5432.

        Heat (7) / cool (8) / hot water (9) are only reported when the
        compressor (or heater bit) is actually running. Otherwise return
        idle-like 6 so climate can show idle instead of a continuous heating
        band during hysteresis. Use get_panel_operating_mode for the panel
        mode text even when effort is 0.
        """
        running = await self.get_run_state()
        if running is None:
            return None
        if not running:
            return 0
        raw = await self._raw_operation_mode()
        if raw is None:
            return None
        # Nordic 5432: 1 cool, 2 heat, 3 dehum, 4 DHW
        if raw == 4:
            effort = await self.get_main_compressor_effort()
            if effort is not None and effort > 0:
                return 9  # Hot water production
            return 6
        if raw == 2:
            active = await self.get_actively_heating()
            if active is True:
                return 7
            return 6
        if raw == 1:
            active = await self.get_actively_cooling()
            if active is True:
                return 8
            return 6
        return 6

    async def get_electric_water_heater_state(self) -> bool | None:
        """Electrical supplement heater (holding 20464, 0/1)."""
        value = await self._read_holding_unsigned(Reg.electrical_supplement_heater)
        if value is None:
            _LOGGER.error("Could not read get_electric_water_heater_state")
            return None
        return bool(value)

    async def set_electric_water_heater_state(self, value: bool | int) -> bool:
        """Write electrical supplement heater holding 20464 (0/1)."""
        on = 1 if value else 0
        return await self._write_holding(Reg.electrical_supplement_heater, on)

    async def get_scalding_protection_setpoint(self) -> float | None:
        """Scalding protection temperature (holding 20463, scale 0.1)."""
        return await self._read_temp_holding(Reg.scalding_protection)

    async def set_scalding_protection_setpoint(self, value: float) -> bool:
        """Set scalding protection (holding 20463)."""
        return await self._write_temp(Reg.scalding_protection, value, 50, 80)

    async def get_el_supplement_activated_below(self) -> float | None:
        """El-supplement activates below this DHW temp (20462, scale 0.1)."""
        return await self._read_temp_holding(Reg.el_supplement_activated_below)

    async def set_el_supplement_activated_below(self, value: float) -> bool:
        """Set el-supplement below threshold (holding 20462)."""
        return await self._write_temp(
            Reg.el_supplement_activated_below, value, 5, 60
        )

    async def get_ventilation_pause(self) -> bool | None:
        """Ventilation pause (holding 20100)."""
        value = await self._read_holding_unsigned(Reg.ventilation_pause)
        if value is None:
            return None
        return bool(value)

    async def set_ventilation_pause(self, value: bool | int) -> bool:
        """Set ventilation pause (holding 20100)."""
        return await self._write_holding(
            Reg.ventilation_pause, 1 if value else 0
        )

    async def get_hot_water_production_pause(self) -> bool | None:
        """DHW production pause (holding 20440)."""
        value = await self._read_holding_unsigned(Reg.pause_hot_water_production)
        if value is None:
            return None
        return bool(value)

    async def set_hot_water_production_pause(self, value: bool | int) -> bool:
        """Set DHW production pause (holding 20440)."""
        return await self._write_holding(
            Reg.pause_hot_water_production, 1 if value else 0
        )

    async def get_hot_water_pause_days(self) -> int | None:
        """DHW pause duration in days (holding 20441)."""
        return await self._read_holding_unsigned(Reg.pause_duration_days)

    async def set_hot_water_pause_days(self, value: int) -> bool:
        """Set DHW pause duration days (holding 20441)."""
        days = int(value)
        if days < 1 or days > 30:
            _LOGGER.error("Nordic DHW pause days %s out of range 1..30", days)
            return False
        return await self._write_holding(Reg.pause_duration_days, days)

    async def get_allow_active_cooling(self) -> bool | None:
        """Allow active cooling (holding 20180)."""
        value = await self._read_holding_unsigned(Reg.allow_active_cooling)
        if value is None:
            return None
        return bool(value)

    async def set_allow_active_cooling(self, value: bool | int) -> bool:
        """Set allow active cooling (holding 20180)."""
        return await self._write_holding(
            Reg.allow_active_cooling, 1 if value else 0
        )

    async def get_low_humidity_level(self) -> int | None:
        """Low humidity strategy threshold % (holding 20160)."""
        return await self._read_holding_unsigned(Reg.low_humidity_level)

    async def set_low_humidity_level(self, value: int) -> bool:
        """Set low humidity level % (holding 20160)."""
        level = int(value)
        if level < 15 or level > 45:
            _LOGGER.error("Nordic low humidity %s out of range 15..45", level)
            return False
        return await self._write_holding(Reg.low_humidity_level, level)

    def _decode_humidity_fan_step(self, value: int | None) -> int | None:
        """Map 101-104 or 1-4 humidity fan encodings to step."""
        if value is None:
            return None
        if 101 <= value <= 104:
            return value - 100
        if value in (0, 1, 2, 3, 4):
            return value
        return None

    async def get_low_humidity_step(self) -> int | None:
        """Fan step at low humidity (holding 20161)."""
        return self._decode_humidity_fan_step(
            await self._read_holding_unsigned(Reg.fan_speed_at_low_humidity)
        )

    async def set_low_humidity_step(self, mode: int) -> bool:
        """Set fan step at low humidity (holding 20161 as 101-104)."""
        step = int(mode)
        if step not in (0, 1, 2, 3, 4):
            return False
        raw = 100 + step if step > 0 else 0
        return await self._write_holding(Reg.fan_speed_at_low_humidity, raw)

    async def get_high_humidity_step(self) -> int | None:
        """Fan step at high humidity (holding 20162)."""
        return self._decode_humidity_fan_step(
            await self._read_holding_unsigned(Reg.fan_speed_at_high_humidity)
        )

    async def set_high_humidity_step(self, mode: int) -> bool:
        """Set fan step at high humidity (holding 20162 as 101-104)."""
        step = int(mode)
        if step not in (0, 2, 3, 4):
            return False
        raw = 100 + step if step > 0 else 0
        return await self._write_holding(Reg.fan_speed_at_high_humidity, raw)

    async def get_max_high_humidity_vent_time(self) -> int | None:
        """Timeout for high humidity ventilation minutes (holding 20163)."""
        return await self._read_holding_unsigned(Reg.timeout_high_humidity)

    async def set_max_high_humidity_vent_time(self, value: int) -> bool:
        """Set high humidity timeout minutes (holding 20163)."""
        minutes = int(value)
        if minutes < 1 or minutes > 180:
            return False
        return await self._write_holding(Reg.timeout_high_humidity, minutes)

    async def get_frost_protection(self) -> bool | None:
        """Polar frost protection enable (holding 20300)."""
        value = await self._read_holding_unsigned(Reg.frost_protection)
        if value is None:
            return None
        return bool(value)

    async def set_frost_protection(self, value: bool | int) -> bool:
        """Set frost protection (holding 20300)."""
        return await self._write_holding(Reg.frost_protection, 1 if value else 0)

    async def get_frost_protection_below(self) -> float | None:
        """Start frost protection below (holding 20340, scale 0.1)."""
        return await self._read_temp_holding(Reg.start_frost_protection_below)

    async def set_frost_protection_below(self, value: float) -> bool:
        """Set frost protection below threshold (holding 20340)."""
        return await self._write_temp(
            Reg.start_frost_protection_below, value, -20, 10
        )

    async def get_preheater_setpoint(self) -> float | None:
        """Preheater setpoint T4 path (holding 20341, scale 0.1)."""
        return await self._read_temp_holding(Reg.set_point_for_pre_heater)

    async def set_preheater_setpoint(self, value: float) -> bool:
        """Set preheater setpoint (holding 20341)."""
        return await self._write_temp(Reg.set_point_for_pre_heater, value, 0, 20)

    async def get_anti_legionella_manual(self) -> bool | None:
        """Manual anti-legionella start flag (holding 20480)."""
        value = await self._read_holding_unsigned(Reg.start_anti_legionella_manual)
        if value is None:
            return None
        return bool(value)

    async def set_anti_legionella_manual(self, value: bool | int) -> bool:
        """Write manual anti-legionella start (holding 20480)."""
        return await self._write_holding(
            Reg.start_anti_legionella_manual, 1 if value else 0
        )

    async def get_automatic_anti_legionella(self) -> bool | None:
        """Automatic anti-legionella (holding 20481)."""
        value = await self._read_holding_unsigned(Reg.automatic_anti_legionella)
        if value is None:
            return None
        return bool(value)

    async def set_automatic_anti_legionella(self, value: bool | int) -> bool:
        """Set automatic anti-legionella (holding 20481)."""
        return await self._write_holding(
            Reg.automatic_anti_legionella, 1 if value else 0
        )

    async def get_legionella_day(self) -> int | None:
        """Day for anti-legionella (holding 20482, 0-7)."""
        return await self._read_holding_unsigned(Reg.day_for_anti_legionella)

    async def set_legionella_day(self, mode: int) -> bool:
        """Set day for anti-legionella (holding 20482)."""
        day = int(mode)
        if day < 0 or day > 7:
            return False
        return await self._write_holding(Reg.day_for_anti_legionella, day)

    async def get_anti_legionella_time(self) -> int | None:
        """Time slot for anti-legionella (holding 20483)."""
        return await self._read_holding_unsigned(Reg.time_for_anti_legionella)

    async def set_anti_legionella_time(self, value: int) -> bool:
        """Set time slot for anti-legionella (holding 20483)."""
        slot = int(value)
        if slot < 0 or slot > 23:
            return False
        return await self._write_holding(Reg.time_for_anti_legionella, slot)
