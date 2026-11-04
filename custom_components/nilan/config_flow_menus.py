"""Config-flow menu labels that stay visible even when translations blank.

A YAML Modbus hub named bare ``nilan`` can collide with this integration
domain and blank ``async_show_menu`` labels that rely only on translation
lookups (issue #6). Passing ``menu_options`` as a dict of id -> label keeps
the five board choices readable. Prefer translated strings when available.
"""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# English fallbacks: never return empty labels to the UI.
MENU_LABELS: dict[str, dict[str, str]] = {
    "menu": {
        "tcp": "TCP",
        "serial": "Serial",
    },
    "board": {
        "auto_detect": "Auto-detect (recommended)",
        "cts602": "CTS602 (Comfort / Compact / VP)",
        "cts700": "CTS700 2018+ Compact P (fan percent 21771)",
        "cts700_nordic": "CTS700 Nordic/Polar/Arctic XL (fan steps 101-104)",
        "cts700_legacy": "CTS700 2015 legacy map",
    },
    "confirm": {
        "accept": "Accept and create entry",
        "manual": "Choose board manually",
    },
}


def _translation_candidates(step_id: str, option_id: str) -> list[str]:
    """Possible keys used by Home Assistant translation helpers."""
    base = f"config.step.{step_id}.menu_options.{option_id}"
    return [
        f"component.{DOMAIN}.{base}",
        f"{DOMAIN}.{base}",
        base,
    ]


async def async_menu_options(
    hass: HomeAssistant,
    step_id: str,
) -> dict[str, str]:
    """Return menu option id -> non-empty label for ``async_show_menu``."""
    defaults = MENU_LABELS.get(step_id)
    if not defaults:
        return {}

    language = getattr(hass.config, "language", None) or "en"
    translations: dict[str, Any] = {}
    try:
        from homeassistant.helpers.translation import async_get_translations

        translations = await async_get_translations(
            hass, language, "config", {DOMAIN}
        )
    except Exception:  # noqa: BLE001 - keep English labels if lookup fails
        _LOGGER.debug(
            "Nilan menu translation lookup failed for %s/%s; using fallbacks",
            language,
            step_id,
            exc_info=True,
        )
        return dict(defaults)

    resolved: dict[str, str] = {}
    for option_id, fallback in defaults.items():
        label = fallback
        for key in _translation_candidates(step_id, option_id):
            value = translations.get(key)
            if isinstance(value, str) and value.strip():
                label = value.strip()
                break
        resolved[option_id] = label
    return resolved
