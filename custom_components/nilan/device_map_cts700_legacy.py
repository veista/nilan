"""CTS700 2015 legacy entity map (MVP)."""

CTS700_LEGACY_ENTITY_MAP = {
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
    "get_humidity": {"entity_type": "sensor"},
    "get_days_to_air_filter_change": {"entity_type": "sensor"},
    "get_electric_water_heater_setpoint": {"entity_type": "config"},
    "get_t11_electric_water_heater_temperature": {"entity_type": "config"},
    "get_electric_water_heater_state": {"entity_type": "config"},
    "get_compressor_water_heater_setpoint": {"entity_type": "config"},
    "get_t12_compressor_water_heater_temperature": {"entity_type": "config"},
}
