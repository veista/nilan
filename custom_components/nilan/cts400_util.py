"""Pure helpers for the CTS400 board.

Deliberately free of Home Assistant and pymodbus imports so the behavioural logic (fan percentage <-> level mapping and signed-register decoding) can be unit-tested without an HA harness.
"""
from __future__ import annotations

SPEED_COUNT = 4
_STEP = 100 / SPEED_COUNT  # 25 % per level


def percentage_to_level(percentage: float) -> int:
    """Map a 0-100 % onto fan level 0-4 (0 = off).

    Uses round-half-up (not Python's banker's rounding) so a value sitting exactly on a .5 boundary rounds to the higher level predictably.
    """
    level = int(percentage / _STEP + 0.5)
    return max(0, min(SPEED_COUNT, level))


def level_to_percentage(level: int) -> int:
    """Map a fan level 1-4 onto its percentage (25/50/75/100)."""
    return int(round(level * _STEP))


def decode_signed16(raw: int) -> int:
    """Reinterpret an unsigned 16-bit register value as a signed int16."""
    return raw - 0x10000 if raw >= 0x8000 else raw
