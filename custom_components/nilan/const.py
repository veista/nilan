"""Constants for the Nilan integration."""

DOMAIN = "nilan"

BOARD_TYPE_CTS602 = "CTS602"
BOARD_TYPE_CTS700 = "CTS700"
BOARD_TYPE_CTS700_LEGACY = "CTS700_LEGACY"
BOARD_TYPE_CTS700_NORDIC = "CTS700_NORDIC"
# CTS400 reserved until a verified Modbus map and dump exist (docs/naering/cts400.md).
#
# Compatibility: each CTS700 board owns its own fan/setpoint writers.
# Probe order: CTS602 -> CTS700_NORDIC (4747 in 101-104) -> CTS700 2018+ -> CTS700_LEGACY.
BOARD_TYPES = (
    BOARD_TYPE_CTS602,
    BOARD_TYPE_CTS700,
    BOARD_TYPE_CTS700_LEGACY,
    BOARD_TYPE_CTS700_NORDIC,
)
