"""Capability profiles and marketing aliases for Nilan catalog coverage.

Profiles gate optional entities. They do not invent Modbus registers.
"""

from __future__ import annotations

from typing import FrozenSet, Mapping

# Capability flag names (match catalog docs)
CAP_VENTILATION = "ventilation"
CAP_PASSIVE_HRV = "passive_hrv"
CAP_ACTIVE_HRV = "active_hrv"
CAP_COMFORT_HEAT = "comfort_heat"
CAP_COMFORT_COOL = "comfort_cool"
CAP_DHW = "dhw"
CAP_SPACE_HEATING = "space_heating"
CAP_GEO = "geo"
CAP_COMMERCIAL_SCALE = "commercial_scale"

ALL_CAPS: FrozenSet[str] = frozenset(
    {
        CAP_VENTILATION,
        CAP_PASSIVE_HRV,
        CAP_ACTIVE_HRV,
        CAP_COMFORT_HEAT,
        CAP_COMFORT_COOL,
        CAP_DHW,
        CAP_SPACE_HEATING,
        CAP_GEO,
        CAP_COMMERCIAL_SCALE,
    }
)

_BASE_VENT = frozenset({CAP_VENTILATION, CAP_PASSIVE_HRV})
_ACTIVE_AIR = _BASE_VENT | frozenset(
    {CAP_ACTIVE_HRV, CAP_COMFORT_HEAT, CAP_COMFORT_COOL}
)
_COMPACT = _ACTIVE_AIR | frozenset({CAP_DHW})
_COMPACT_GEO = _COMPACT | frozenset({CAP_GEO, CAP_SPACE_HEATING})
_VP_WATER = _ACTIVE_AIR | frozenset({CAP_DHW})
_VGU = frozenset({CAP_DHW, CAP_SPACE_HEATING, CAP_VENTILATION})
_COMMERCIAL_PASSIVE = _BASE_VENT | frozenset({CAP_COMMERCIAL_SCALE})
_COMMERCIAL_ACTIVE = _ACTIVE_AIR | frozenset({CAP_COMMERCIAL_SCALE})

# CTS602 control_type id -> capability set
CTS602_CAPABILITIES: Mapping[int, FrozenSet[str]] = {
    2: _BASE_VENT,  # Comfort light
    3: _ACTIVE_AIR,  # Comfort Polar
    4: _ACTIVE_AIR,  # VPL 15c
    10: _COMPACT,  # CompactS
    11: _VP_WATER,  # VP 18comp
    12: _VP_WATER,  # VP18cCom
    13: _BASE_VENT,  # COMFORT
    19: _VP_WATER,  # VP 18c
    20: _VP_WATER,  # VP 18ek
    21: _VP_WATER,  # VP 18cek
    25: _ACTIVE_AIR,  # VPL 25c
    26: _ACTIVE_AIR | frozenset({CAP_COMMERCIAL_SCALE}),  # VPM/28EC
    28: _VP_WATER,  # VP18cCoB
    30: _COMPACT,  # COMPACTn
    31: _BASE_VENT,  # COMFORTn
    32: _VP_WATER,  # VP18 M2
    33: _ACTIVE_AIR,  # COMBI 300 N
    35: _ACTIVE_AIR,  # COMBI 302
    36: _ACTIVE_AIR,  # COMBI 302 T
    38: _VGU,  # VGU180 ek
    42: _COMMERCIAL_PASSIVE,  # VENTEC
    44: _COMPACT,  # CompactP (AIR/GEO refined below)
}

CTS700_CAPABILITIES: FrozenSet[str] = _COMPACT
CTS700_LEGACY_CAPABILITIES: FrozenSet[str] = _COMPACT
CTS700_NORDIC_CAPABILITIES: FrozenSet[str] = _COMPACT

# Marketing / plate aliases -> HMI name and optional type id
MARKETING_ALIASES: Mapping[str, Mapping[str, object]] = {
    "comfort ct200": {"hmi": "Comfort light", "type_id": 2},
    "comfort ct500": {"hmi": "COMFORTn", "type_id": 31},
    "comfort 200 top": {"hmi": "COMFORTn", "type_id": 31},
    "comfort 250 top": {"hmi": "COMFORTn", "type_id": 31},
    "comfort 350 top": {"hmi": "COMFORTn", "type_id": 31},
    "comfort 300lr": {"hmi": "COMFORTn", "type_id": 31},
    "comfort 250l": {"hmi": "COMFORTn", "type_id": 31},
    "comfort 250r": {"hmi": "COMFORTn", "type_id": 31},
    "comfort 350l": {"hmi": "COMFORTn", "type_id": 31},
    "comfort 350r": {"hmi": "COMFORTn", "type_id": 31},
    "comfort 450": {"hmi": "COMFORTn", "type_id": 31},
    "comfort 600": {"hmi": "CTS602 commercial", "type_id": None},
    "comfort 1200": {"hmi": "CTS602 commercial", "type_id": None},
    "comfort 5000": {"hmi": "CTS602 commercial", "type_id": None},
    "combi 302 polar": {"hmi": "COMBI 302", "type_id": 35},
    "combi 302 polar top": {"hmi": "COMBI 302 T", "type_id": 36},
    "combi s 302 polar top": {"hmi": "COMBI 300 N", "type_id": 33},
    "combi 400 polar top": {"hmi": "unknown", "type_id": None},
    "vpl 15": {"hmi": "VPL 15c", "type_id": 4},
    "vpl 15 top m2": {"hmi": "VPL 15c", "type_id": 4},
    "vpl 28": {"hmi": "VPM/28EC", "type_id": 26},
    "compact s": {"hmi": "CompactS", "type_id": 10},
    "compact p2": {"hmi": "CompactP", "type_id": 44, "board": "CTS602"},
    "compact p2 air": {"hmi": "CompactP", "type_id": 44, "board": "CTS602"},
    "compact p2 air e-silent": {"hmi": "CompactP", "type_id": 44, "board": "CTS602"},
    "compact p2 ek": {"hmi": "CompactP", "type_id": 44, "board": "CTS602"},
    "compact p2 geo3": {"hmi": "CompactP", "type_id": 44, "board": "CTS602"},
    "compact p2 geo6": {"hmi": "CompactP", "type_id": 44, "board": "CTS602"},
    "compact p2 geo9": {"hmi": "CompactP", "type_id": 44, "board": "CTS602"},
    "compact p": {"hmi": "CompactP or CTS700", "type_id": 44},
    "compact p air": {"hmi": "CompactP or CTS700", "type_id": 44},
    "compact p ek": {"hmi": "CompactP or CTS700", "type_id": 44},
    "compact p geo": {"hmi": "CompactP", "type_id": 44},
    "compact p nordic": {"hmi": "CompactP or CTS700", "type_id": 44},
    # Catalog CTS602 type 44 (RS485) vs CTS700 LC Ethernet hybrids below
    "compact p xl nordic": {
        "hmi": "CompactP or CTS700_NORDIC",
        "type_id": 44,
    },
    "compact p nordic xl": {
        "hmi": "CompactP or CTS700_NORDIC",
        "type_id": 44,
    },
    "compact p xl nordic rf": {
        "hmi": "CTS700_NORDIC",
        "type_id": 44,
    },
    "compact p nordic xl rf": {
        "hmi": "CTS700_NORDIC",
        "type_id": 44,
    },
    "nordic xl rf": {
        "hmi": "CTS700_NORDIC",
        "type_id": 44,
    },
    # Nilan wiring / produktliste: Compact P Køl (Sol) Polar/Nordic/Arctic (XL)
    # CTS700 LC Board Version 4.0, varenr 75124xx, styreprint #237501
    "compact p køl polar nordic arctic xl": {
        "hmi": "CTS700_NORDIC",
        "type_id": None,
        "board": "CTS700_NORDIC",
    },
    "compact p kol polar nordic arctic xl": {
        "hmi": "CTS700_NORDIC",
        "type_id": None,
        "board": "CTS700_NORDIC",
    },
    "compact p koel polar nordic arctic xl": {
        "hmi": "CTS700_NORDIC",
        "type_id": None,
        "board": "CTS700_NORDIC",
    },
    "compact p polar xl": {
        "hmi": "CTS700_NORDIC",
        "type_id": None,
        "board": "CTS700_NORDIC",
    },
    "compact p arctic xl": {
        "hmi": "CTS700_NORDIC",
        "type_id": None,
        "board": "CTS700_NORDIC",
    },
    "compact p nordic arctic xl": {
        "hmi": "CTS700_NORDIC",
        "type_id": None,
        "board": "CTS700_NORDIC",
    },
    "ncs-700": {
        "hmi": "CTS700_NORDIC or CTS700",
        "type_id": None,
        "board": "CTS700",
    },
    "ncs-700 lc board": {
        "hmi": "CTS700_NORDIC or CTS700",
        "type_id": None,
        "board": "CTS700",
    },
    "cts700 lc board": {
        "hmi": "CTS700_NORDIC or CTS700",
        "type_id": None,
        "board": "CTS700",
    },
    "compact p xl polar": {
        "hmi": "CTS700_NORDIC",
        "type_id": None,
        "board": "CTS700_NORDIC",
    },
    "vp 18 m2": {"hmi": "VP18 M2", "type_id": 32},
    "vp 18 m2 ek": {"hmi": "VP 18ek", "type_id": 20},
    "vgu 180 ek": {"hmi": "VGU180 ek", "type_id": 38},
    "vgu 250 m2 nordic": {"hmi": "unknown", "type_id": None},
}


def capabilities_for_cts602(type_id: int, air_geo_type: int = 0) -> FrozenSet[str]:
    """Return capability flags for a CTS602 HMI type."""
    caps = set(CTS602_CAPABILITIES.get(type_id, _BASE_VENT))
    if type_id == 44:
        if air_geo_type == 2:
            caps = set(_COMPACT_GEO)
        else:
            caps = set(_COMPACT)
            caps.discard(CAP_GEO)
            caps.discard(CAP_SPACE_HEATING)
    return frozenset(caps)


def capabilities_for_cts700() -> FrozenSet[str]:
    """Return capability flags for CTS700 Compact P MVP maps."""
    return CTS700_CAPABILITIES


def capabilities_for_cts700_legacy() -> FrozenSet[str]:
    """Return capability flags for CTS700 2015 legacy map."""
    return CTS700_LEGACY_CAPABILITIES


def capabilities_for_cts700_nordic() -> FrozenSet[str]:
    """Return capability flags for CTS700 Nordic XL hybrid map."""
    return CTS700_NORDIC_CAPABILITIES


def entity_allowed(
    entity_meta: Mapping[str, object], caps: FrozenSet[str]
) -> bool:
    """True if entity metadata is allowed for the device capability set."""
    required = entity_meta.get("requires_capabilities")
    if not required:
        return True
    if isinstance(required, str):
        required_set = {required}
    else:
        required_set = set(required)
    return required_set.issubset(caps)


def lookup_marketing_alias(name: str) -> Mapping[str, object] | None:
    """Lookup marketing alias (case-insensitive)."""
    if not name:
        return None
    key = " ".join(name.strip().lower().split())
    return MARKETING_ALIASES.get(key)


def filter_attributes_by_capabilities(
    attributes: dict, entity_map: Mapping[str, Mapping[str, object]], caps: FrozenSet[str]
) -> dict:
    """Drop attributes whose entity map requires missing capabilities."""
    out = {}
    for key, entity_type in attributes.items():
        meta = entity_map.get(key)
        if meta is None or entity_allowed(meta, caps):
            out[key] = entity_type
    return out
