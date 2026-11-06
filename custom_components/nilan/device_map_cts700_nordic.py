"""CTS700 Compact P Køl Polar/Nordic/Arctic (XL) hybrid entity map.

Aligned with mark007 Modbus YAML + Nilan CTS700 LC Board v4.0 wiring
(T1–T12 physical sensors on Compact P Køl Polar/Nordic/Arctic XL).
"""

CTS700_NORDIC_ENTITY_MAP = {
    "get_run_state": {"entity_type": "config"},
    "get_operation_mode": {"entity_type": "config"},
    "get_ventilation_step": {"entity_type": "config"},
    "get_control_state": {"entity_type": "sensor"},
    "get_user_temperature_setpoint": {"entity_type": "config"},
    "get_control_temperature": {"entity_type": "config"},
    "get_t1_intake_temperature": {"entity_type": "sensor"},
    "get_t2_inlet_temperature": {"entity_type": "sensor"},
    "get_t3_exhaust_temperature": {"entity_type": "sensor"},
    "get_t4_outlet": {"entity_type": "sensor"},
    "get_t5_condenser_temperature": {"entity_type": "sensor"},
    "get_t6_evaporator_temperature": {"entity_type": "sensor"},
    "get_t7_inlet_temperature_after_heater": {"entity_type": "sensor"},
    "get_t8_outdoor_temperature": {"entity_type": "sensor"},
    "get_t9_heater_temperature": {"entity_type": "sensor"},
    "get_humidity": {"entity_type": "sensor"},
    "get_average_humidity": {"entity_type": "sensor"},
    "get_days_to_inlet_filter_change": {"entity_type": "sensor"},
    "get_days_since_inlet_filter_change": {"entity_type": "sensor"},
    "get_days_to_exhaust_filter_change": {"entity_type": "sensor"},
    "get_days_since_exhaust_filter_change": {"entity_type": "sensor"},
    "get_filter_interval_inlet": {"entity_type": "sensor"},
    "get_filter_interval_exhaust": {"entity_type": "sensor"},
    "get_filter_alarm_state": {"entity_type": "binary_sensor"},
    # Bypass: status only (Ethernet writes on 21773 are unreliable).
    "get_bypass_flap_state": {"entity_type": "binary_sensor"},
    "get_bypass_damper_percent": {"entity_type": "sensor"},
    "get_fan_speed_percent": {"entity_type": "sensor"},
    "get_supply_fan_speed": {"entity_type": "sensor"},
    "get_return_fan_speed": {"entity_type": "sensor"},
    "get_anode_state": {"entity_type": "sensor"},
    "get_electric_water_heater_setpoint": {
        "entity_type": "config",
        "requires_capabilities": "dhw",
    },
    "get_t11_electric_water_heater_temperature": {
        "entity_type": "config",
        "requires_capabilities": "dhw",
    },
    # Stay config (water_heater status only). Do not map Compact P 20464 as switch.
    "get_electric_water_heater_state": {
        "entity_type": "config",
        "requires_capabilities": "dhw",
    },
    "get_compressor_water_heater_setpoint": {
        "entity_type": "config",
        "requires_capabilities": "dhw",
    },
    "get_t12_compressor_water_heater_temperature": {
        "entity_type": "config",
        "requires_capabilities": "dhw",
    },
}
