"""Setup-time register probe for the Nilan integration.

Nilan board families (CTS602, CTS700 2018+, CTS700 2015 legacy, CTS700 Nordic
hybrid) share hardware generations but support different register subsets per
firmware variant. Probing every optional register at setup tells the
integration which entities can work on THIS unit. Dead registers are recorded
per device; getters short-circuit on them so no Modbus call (and no error log)
is ever made again. Entity platforms disable-by-default attributes whose
registers did not respond.

Register definitions are never removed here: a register dead on one unit may
be live on another. This file only controls whether it is polled.
"""

from __future__ import annotations

import logging
from typing import Any

_LOGGER = logging.getLogger(__name__)

# Board type key -> {attribute: [(kind, address), ...]}
# kind: "holding" | "input". Only UNCERTAIN registers are listed. Core
# registers (machine type, T1/T3 probes, setpoints) stay out — they are
# required and already fail setup when absent.
PROBE_SPECS: dict[str, dict[str, list[tuple[str, int]]]] = {
    # CTS700 Nordic/Polar/Arctic hybrid (20xxx holding space absent on
    # firmware 2.03.01.14; 1xxx-5xxx space live).
    "CTS700_NORDIC": {
        "get_average_humidity": [("holding", 20164)],
        "get_t4_outlet": [("holding", 20288)],
        "get_t5_condenser_temperature": [("holding", 20290)],
        "get_t6_evaporator_temperature": [("holding", 20292)],
        "get_t7_inlet_temperature_after_heater": [("holding", 20294)],
        "get_t8_outdoor_temperature": [("input", 5159), ("holding", 20296)],
        "get_t9_heater_temperature": [("holding", 20298)],
        "get_fan_speed_percent": [("holding", 21771)],
        "get_bypass_flap_state": [("holding", 4704), ("holding", 21773)],
        "get_bypass_damper_percent": [("holding", 21773)],
        "get_main_compressor_effort": [("holding", 4706)],
        "get_heat_pump_state": [("holding", 4706)],
        "get_electric_water_heater_setpoint": [("holding", 20460)],
        "get_electric_water_heater_state": [("holding", 20464)],
        "get_scalding_protection_setpoint": [("holding", 20463)],
        "get_el_supplement_activated_below": [("holding", 20462)],
        "get_ventilation_pause": [("holding", 20100)],
        "get_hot_water_production_pause": [("holding", 20440)],
        "get_hot_water_pause_days": [("holding", 20441)],
        "get_allow_active_cooling": [("holding", 20180)],
        "get_low_humidity_level": [("holding", 20160)],
        "get_low_humidity_step": [("holding", 20161)],
        "get_high_humidity_step": [("holding", 20162)],
        "get_max_high_humidity_vent_time": [("holding", 20163)],
        "get_frost_protection": [("holding", 20300)],
        "get_frost_protection_below": [("holding", 20340)],
        "get_preheater_setpoint": [("holding", 20341)],
        "get_anti_legionella_manual": [("holding", 20480)],
        "get_automatic_anti_legionella": [("holding", 20481)],
        "get_legionella_day": [("holding", 20482)],
        "get_anti_legionella_time": [("holding", 20483)],
        "get_days_to_inlet_filter_change": [
            ("holding", 1328),
            ("holding", 20103),
        ],
        "get_days_since_inlet_filter_change": [
            ("holding", 1326),
            ("holding", 1328),
        ],
        "get_days_to_exhaust_filter_change": [("holding", 1329)],
        "get_days_since_exhaust_filter_change": [
            ("holding", 1327),
            ("holding", 1329),
        ],
        "get_filter_interval_inlet": [("holding", 1326)],
        "get_filter_interval_exhaust": [("holding", 1327)],
    },
    # CTS700 2018+ Compact P.
    "CTS700": {
        "get_ventilation_step": [("holding", 21771)],
        "get_t8_outdoor_temperature": [("holding", 20296)],
        "get_days_to_air_filter_change": [("holding", 20103)],
    },
    # CTS700 2015 legacy.
    "CTS700_LEGACY": {
        "get_days_to_air_filter_change": [
            ("holding", 1326),
            ("holding", 1328),
        ],
    },
    # CTS602 (incl. Comfort light).
    "CTS602": {
        "get_t15_user_panel_temperature": [("input", 215)],
        "get_user_function_1_state": [("holding", 123)],
        "get_user_function_2_state": [("holding", 124)],
    },
}


async def run_register_probe(device: Any, spec: dict) -> None:
    """Probe registers once, fill dead/unsupported sets on the device.

    Mutates device._dead_registers (set[(kind, address)]) and
    device._unsupported_attributes (set[str]).
    """
    dead: set[tuple[str, int]] = set()
    for _attr, regs in spec.items():
        for kind, address in regs:
            result = await device._modbus.async_pb_call(
                device._unit_id, address, 1, kind
            )
            if result is None:
                dead.add((kind, address))

    device._dead_registers = dead
    device._unsupported_attributes = {
        attr
        for attr, regs in spec.items()
        if all((kind, address) in dead for kind, address in regs)
    }

    for kind, address in sorted(dead):
        _LOGGER.warning(
            "register %s %s unsupported on this unit — entity may be disabled",
            kind,
            address,
        )


def serialize_dead_registers(
    dead: set[tuple[str, int]],
) -> list[list[str | int]]:
    """JSON-safe form for config entry storage."""
    return sorted([[kind, address] for kind, address in dead])


def deserialize_dead_registers(stored: list) -> set[tuple[str, int]]:
    """Restore dead register set from stored form."""
    return {(str(kind), int(address)) for kind, address in stored}
