"""CTS700 Compact P 2018+ entity map (MVP).

Fan/setpoint stay on 21771 / 20102 / 20286. Safe 20xxx extras only; never
Nordic 4747 step encoding (101-104) on this board path.
"""

CTS700_ENTITY_MAP = {
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
    "get_t8_outdoor_temperature": {"entity_type": "sensor"},
    "get_humidity": {"entity_type": "sensor"},
    "get_days_to_air_filter_change": {"entity_type": "sensor"},
    "get_electric_water_heater_setpoint": {
        "entity_type": "config",
        "requires_capabilities": "dhw",
    },
    "get_t11_electric_water_heater_temperature": {
        "entity_type": "config",
        "requires_capabilities": "dhw",
    },
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
}
