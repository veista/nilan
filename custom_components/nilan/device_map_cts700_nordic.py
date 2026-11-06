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
    # Heat pump / main compressor effort (holding 4706); on when effort > 0.
    "get_main_compressor_effort": {"entity_type": "sensor"},
    "get_heat_pump_state": {"entity_type": "binary_sensor"},
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
    # Holding 20464: writable electrical supplement (live-validated on Nordic).
    "get_electric_water_heater_state": {
        "entity_type": "switch",
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
    # DHW / el-supplement thresholds
    "get_scalding_protection_setpoint": {
        "entity_type": "number",
        "requires_capabilities": "dhw",
    },
    "get_el_supplement_activated_below": {
        "entity_type": "number",
        "requires_capabilities": "dhw",
    },
    # Pauses
    "get_ventilation_pause": {"entity_type": "switch"},
    "get_hot_water_production_pause": {
        "entity_type": "switch",
        "requires_capabilities": "dhw",
    },
    "get_hot_water_pause_days": {
        "entity_type": "number",
        "requires_capabilities": "dhw",
    },
    # Cooling + humidity strategy
    "get_allow_active_cooling": {"entity_type": "switch"},
    "get_low_humidity_level": {"entity_type": "number"},
    "get_low_humidity_step": {"entity_type": "select"},
    "get_high_humidity_step": {"entity_type": "select"},
    "get_max_high_humidity_vent_time": {"entity_type": "number"},
    # Polar frost / preheat
    "get_frost_protection": {"entity_type": "switch"},
    "get_frost_protection_below": {"entity_type": "number"},
    "get_preheater_setpoint": {"entity_type": "number"},
    # Anti-legionella
    "get_anti_legionella_manual": {
        "entity_type": "switch",
        "requires_capabilities": "dhw",
    },
    "get_automatic_anti_legionella": {
        "entity_type": "switch",
        "requires_capabilities": "dhw",
    },
    "get_legionella_day": {
        "entity_type": "select",
        "requires_capabilities": "dhw",
    },
    "get_anti_legionella_time": {
        "entity_type": "number",
        "requires_capabilities": "dhw",
    },
}
