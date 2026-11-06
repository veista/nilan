"""CTS700 Nordic temperature, filter, fan, bypass, and DHW sensors."""

from __future__ import annotations

import logging

from .registers import CTS700NordicRegisters as Reg

_LOGGER = logging.getLogger(__name__)


class CTS700NordicSensorsMixin:
    """Mixin: T-sensors, humidity, filters, fans, bypass, DHW setpoints."""

    async def get_control_temperature(self) -> float | None:
        """Room / extract air temperature (T3 input)."""
        value = await self._read_temp_input(Reg.t3_extract)
        if value is None:
            _LOGGER.error("Could not read get_control_temperature")
        return value

    async def get_user_temperature_setpoint(self) -> float | None:
        """Room temperature setpoint (4746)."""
        value = await self._read_temp_holding(Reg.user_temperature)
        if value is None:
            _LOGGER.error("Could not read get_user_temperature_setpoint")
        return value

    async def set_user_temperature_setpoint(self, value: float) -> bool:
        """Set room temperature setpoint (holding 4746)."""
        return await self._write_temp(Reg.user_temperature, value, 5, 30)

    async def get_t1_intake_temperature(self) -> float | None:
        """Outdoor air temperature."""
        return await self._read_temp_input(Reg.t1_outdoor)

    async def get_t2_inlet_temperature(self) -> float | None:
        """Supply air temperature."""
        return await self._read_temp_input(Reg.t2_supply)

    async def get_t3_exhaust_temperature(self) -> float | None:
        """Extract air temperature."""
        return await self._read_temp_input(Reg.t3_extract)

    async def get_t4_outlet(self) -> float | None:
        """Exhaust / after heat exchanger."""
        return await self._read_temp_holding(Reg.t4_exhaust)

    async def get_t5_condenser_temperature(self) -> float | None:
        """Condenser / after heat pump."""
        return await self._read_temp_holding(Reg.t5_condenser)

    async def get_t6_evaporator_temperature(self) -> float | None:
        """Evaporator temperature (T6)."""
        return await self._read_temp_holding(Reg.t6_evaporator)

    async def get_t7_inlet_temperature_after_heater(self) -> float | None:
        """Supply after after-heater (T7). None when register unused (~0 C)."""
        value = await self._read_temp_holding(Reg.t7_after_heater)
        if value is None:
            return None
        # Many Compact P Nordic/Polar units have no T7 sensor; bus returns 0.0
        if abs(value) < 0.05:
            return None
        return value

    async def get_t8_outdoor_temperature(self) -> float | None:
        """T8 outdoor / preheater path.

        Primary: input 5159 (wiring T8). Some Compact P firmwares also expose
        holding 20296. When 5159 tracks T1 exactly, try 20296 so HA is not
        showing a duplicated outdoor reading by mistake.
        """
        t1 = await self.get_t1_intake_temperature()
        t8_input = await self._read_temp_input(Reg.t8_preheater)
        t8_hold = await self._read_temp_holding(Reg.t8_before_preheater_holding)

        if t8_input is not None and t1 is not None and abs(t8_input - t1) < 0.15:
            if t8_hold is not None and abs(t8_hold - t1) >= 0.15:
                _LOGGER.debug(
                    "CTS700 Nordic T8: input 5159 mirrors T1 (%.1f); using holding 20296 (%.1f)",
                    t1,
                    t8_hold,
                )
                return t8_hold
            _LOGGER.debug(
                "CTS700 Nordic T8 equals T1 (%.1f C); expected when both are outdoor "
                "NTCs and preheater is idle",
                t1,
            )
            return t8_input

        if t8_input is not None:
            return t8_input
        return t8_hold

    async def get_t9_heater_temperature(self) -> float | None:
        """Water surface / after heater (T9, holding 20298)."""
        return await self._read_temp_holding(Reg.t9_water_surface)

    async def get_humidity(self) -> float | None:
        """Live extract humidity (4716)."""
        value = await self._read_input_unsigned(Reg.humidity_live)
        if value is None:
            _LOGGER.error("Could not read get_humidity")
            return None
        return float(value)

    async def get_average_humidity(self) -> float | None:
        """Long-average humidity (20164)."""
        value = await self._read_holding_unsigned(Reg.average_humidity)
        if value is None:
            return None
        return float(value)

    async def get_days_to_inlet_filter_change(self) -> int | None:
        """Days until inlet filter change (holding 1328 remaining; 20103 fallback)."""
        remaining = await self._read_holding_unsigned(Reg.filter_remaining_inlet)
        if remaining is not None:
            return remaining
        return await self._read_holding_unsigned(Reg.filter_days)

    async def get_days_since_inlet_filter_change(self) -> int | None:
        """Days since last inlet filter change (interval - remaining)."""
        interval = await self._read_holding_unsigned(Reg.filter_interval_inlet)
        remaining = await self._read_holding_unsigned(Reg.filter_remaining_inlet)
        if interval is None or remaining is None:
            return None
        return max(0, interval - remaining)

    async def get_days_to_exhaust_filter_change(self) -> int | None:
        """Days until exhaust filter change (holding 1329 remaining)."""
        return await self._read_holding_unsigned(Reg.filter_remaining_exhaust)

    async def get_days_since_exhaust_filter_change(self) -> int | None:
        """Days since last exhaust filter change (interval - remaining)."""
        interval = await self._read_holding_unsigned(Reg.filter_interval_exhaust)
        remaining = await self._read_holding_unsigned(Reg.filter_remaining_exhaust)
        if interval is None or remaining is None:
            return None
        return max(0, interval - remaining)

    async def get_filter_interval_inlet(self) -> int | None:
        """Inlet filter interval in days (holding 1326)."""
        return await self._read_holding_unsigned(Reg.filter_interval_inlet)

    async def get_filter_interval_exhaust(self) -> int | None:
        """Exhaust filter interval in days (holding 1327)."""
        return await self._read_holding_unsigned(Reg.filter_interval_exhaust)

    async def get_filter_alarm_state(self) -> bool | None:
        """Filter alarm active (input 5168)."""
        value = await self._read_input_unsigned(Reg.filter_alarm)
        if value is None:
            _LOGGER.warning(
                "Filter alarm read failed (input %s). Keeping previous HA state; "
                "check Ethernet Modbus load / overlapping YAML hub.",
                Reg.filter_alarm,
            )
            return None
        active = bool(value)
        prev = self._attributes.get("filter_alarm_state")
        if prev is not None and bool(prev) != active:
            _LOGGER.info(
                "Filter alarm changed: %s -> %s (raw=%s, input %s)",
                "ON" if prev else "OFF",
                "ON" if active else "OFF",
                value,
                Reg.filter_alarm,
            )
        elif active:
            _LOGGER.debug(
                "Filter alarm still ON (raw=%s, input %s)",
                value,
                Reg.filter_alarm,
            )
        self._attributes["filter_alarm_state"] = active
        return active

    async def get_fan_speed_percent(self) -> int | None:
        """Fan power / max percent (21771)."""
        return await self._read_holding_unsigned(Reg.fan_power_percent)

    async def get_bypass_damper_percent(self) -> int | None:
        """Bypass damper readout percent (holding 21773). Status only."""
        return await self._read_holding_unsigned(Reg.bypass_damper_percent)

    async def get_main_compressor_effort(self) -> int | None:
        """Main compressor / heat-pump effort percent (holding 4706).

        Community maps and mark007 YAML treat this as 0 when the heat pump is
        off and a positive percent (often up to 100) when the compressor runs.
        Useful as a live "is the heat pump on" signal on Compact P Nordic.
        """
        return await self._read_holding_unsigned(Reg.main_compressor_effort)

    async def get_heat_pump_state(self) -> bool | None:
        """Heat pump running derived from main compressor effort (4706 > 0)."""
        effort = await self.get_main_compressor_effort()
        if effort is None:
            return None
        return effort > 0

    async def get_bypass_flap_state(self) -> bool | None:
        """Bypass open/closed status (read-only).

        Prefer discrete holding 4704 (bypass 1). Fall back to 21773 percent.
        Do not expose a writable switch: Ethernet writes to 21773 often fail
        to stick on Compact P Nordic (see docs/cts700/ethernet-limits.md).
        """
        state = await self._read_holding_unsigned(Reg.bypass_1_state)
        if state is not None:
            return bool(state)
        pct = await self._read_holding_unsigned(Reg.bypass_damper_percent)
        if pct is None:
            _LOGGER.debug(
                "CTS700 Nordic bypass status unavailable (4704/21773). "
                "YAML Modbus coils stay unavailable while that hub is disabled."
            )
            return None
        return pct > 0

    async def get_supply_fan_speed(self) -> int | None:
        """Supply fan actual percent."""
        return await self._read_holding_unsigned(Reg.supply_fan_speed)

    async def get_return_fan_speed(self) -> int | None:
        """Extract fan actual percent."""
        return await self._read_holding_unsigned(Reg.extract_fan_speed)

    async def get_anode_state(self) -> int | None:
        """Anode status raw (0/1/2)."""
        return await self._read_holding_unsigned(Reg.anode_status)

    async def get_electric_water_heater_setpoint(self) -> float | None:
        """DHW setpoint."""
        return await self._read_temp_holding(Reg.hot_water_set_point)

    async def set_electric_water_heater_setpoint(self, value: float) -> bool:
        """Set DHW setpoint (holding 20460)."""
        if value == 0:
            return await self._write_holding(Reg.hot_water_set_point, 0)
        return await self._write_temp(Reg.hot_water_set_point, value, 5, 85)

    async def get_compressor_water_heater_setpoint(self) -> float | None:
        """Shared DHW setpoint."""
        return await self.get_electric_water_heater_setpoint()

    async def set_compressor_water_heater_setpoint(self, value: float) -> bool:
        """Set shared DHW setpoint."""
        return await self.set_electric_water_heater_setpoint(value)

    async def get_t11_electric_water_heater_temperature(self) -> float | None:
        """DHW top temperature."""
        return await self._read_temp_input(Reg.t11_dhw_top)

    async def get_t12_compressor_water_heater_temperature(self) -> float | None:
        """DHW bottom temperature."""
        return await self._read_temp_input(Reg.t12_dhw_bottom)
