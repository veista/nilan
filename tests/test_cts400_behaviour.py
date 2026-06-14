"""CTS400 behavioural unit tests for the pure helpers (no hardware, no HA)."""
from custom_components.nilan.cts400_util import (
    decode_signed16,
    level_to_percentage,
    percentage_to_level,
)


def test_percentage_to_level_slider_multiples():
    # The HA tile emits multiples of 25 for a 4-speed fan.
    assert percentage_to_level(0) == 0
    assert percentage_to_level(25) == 1
    assert percentage_to_level(50) == 2
    assert percentage_to_level(75) == 3
    assert percentage_to_level(100) == 4


def test_percentage_to_level_half_boundaries_round_up():
    # Round-half-up (not banker's rounding): .5 boundaries go to the higher
    # level predictably.
    assert percentage_to_level(12.5) == 1
    assert percentage_to_level(37.5) == 2
    assert percentage_to_level(62.5) == 3
    assert percentage_to_level(87.5) == 4


def test_percentage_to_level_clamped():
    assert percentage_to_level(-10) == 0
    assert percentage_to_level(200) == 4


def test_level_to_percentage_roundtrip():
    for level in (1, 2, 3, 4):
        assert level_to_percentage(level) == level * 25
        assert percentage_to_level(level_to_percentage(level)) == level


def test_decode_signed16():
    assert decode_signed16(0) == 0
    assert decode_signed16(100) == 100        # 10.0 C raw
    assert decode_signed16(0x7FFF) == 32767
    assert decode_signed16(0x8000) == -32768
    assert decode_signed16(0xFFFF) == -1
    # A real negative outdoor temperature: -5.0 C is raw -50 = 0xFFCE.
    assert decode_signed16(0xFFCE) == -50
