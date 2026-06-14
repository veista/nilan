"""CTS400 register-map parity (no hardware, no HA import)."""
from custom_components.nilan.registers import (
    CTS400HoldingRegisters as H,
    CTS400InputRegisters as I,
)

# ES1077/CTS400 protocol document, section 4 (verified on a live unit).
DOC_INPUT = {
    "bypass_open": 23, "extract_air_pct": 24, "supply_air_pct": 25,
    "after_heat_pct": 26, "t1_outdoor": 27, "t2_supply": 28, "t3_extract": 29,
    "t4_exhaust": 30, "humidity": 31, "avg_humidity": 46, "co2": 47, "voc": 48,
    "filter_change": 49, "alarm_status": 50, "alarm_code_1": 51,
    "alarm_code_2": 52, "alarm_code_3": 53, "fan_level": 63, "mode_winter": 72,
    "after_heating": 74, "deicing": 91, "filter_days_remaining": 110,
}
DOC_HOLDING = {
    "reset_alarm": 30, "wanted_room_temp": 37, "summer_winter_threshold": 45,
    "extra_sensor": 48, "filter_interval": 50, "reset_filter_timer": 51,
    "heater_select": 53, "fan_level_set": 69, "run_stop": 70,
}


def test_input_registers_match_protocol_doc():
    for name, addr in DOC_INPUT.items():
        assert getattr(I, name) == addr, name


def test_holding_registers_match_protocol_doc():
    for name, addr in DOC_HOLDING.items():
        assert getattr(H, name) == addr, name


def test_no_duplicate_addresses_within_a_space():
    for cls in (I, H):
        addrs = [v for k, v in vars(cls).items() if not k.startswith("_")
                 and isinstance(v, int)]
        assert len(addrs) == len(set(addrs)), f"duplicate in {cls.__name__}"


def test_shared_numbers_are_cross_space_only():
    # These addresses legitimately exist in BOTH spaces with different meanings (input vs holding): 30 (T4 / reset alarm), 48 (VOC / extra sensor), 51 (alarm code 1 / reset filter timer), 53 (alarm code 3 / heater select).
    for addr in (30, 48, 51, 53):
        assert addr in DOC_INPUT.values()
        assert addr in DOC_HOLDING.values()
