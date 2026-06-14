"""CTS400 entity-map <-> Device methods <-> translations consistency."""
import ast
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1] / "custom_components" / "nilan"


def _methods(pyfile: str) -> set[str]:
    tree = ast.parse((ROOT / pyfile).read_text(encoding="utf-8"))
    return {n.name for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}


def _cts400_entity_map_keys() -> set[str]:
    tree = ast.parse((ROOT / "device_map.py").read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if (isinstance(node, ast.Assign)
                and any(getattr(t, "id", "") == "CTS400_ENTITY_MAP"
                        for t in node.targets)):
            return {k.value for k in node.value.keys}
    raise AssertionError("CTS400_ENTITY_MAP not found")


def _referenced_cts400_names() -> set[str]:
    """All cts400_* entity names referenced by the platform modules.

    These are the string literals used as a Map's name / translation_key (e.g. "cts400_outdoor_temperature", "cts400_ventilation"). Entity-map keys in device_map.py are get_/set_ prefixed and so do not match.
    """
    names: set[str] = set()
    for pyfile in ("sensor.py", "binary_sensor.py", "switch.py",
                   "number.py", "button.py", "fan.py", "climate.py"):
        path = ROOT / pyfile
        if not path.exists():
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if (isinstance(node, ast.Constant)
                    and isinstance(node.value, str)
                    and node.value.startswith("cts400_")):
                names.add(node.value)
    return names


def test_entity_map_keys_are_device_methods():
    methods = _methods("device.py")
    for key in _cts400_entity_map_keys():
        assert key in methods, f"{key} has no Device method"


def test_cts400_entity_names_have_translations():
    en = json.loads((ROOT / "translations" / "en.json").read_text("utf-8"))
    strings = json.loads((ROOT / "strings.json").read_text("utf-8"))

    # collect every cts400_* leaf name across both files' entity sections
    def cts400_names(blob):
        out = set()
        for section in blob.get("entity", {}).values():
            for key in section:
                if key.startswith("cts400_"):
                    out.add(key)
        return out

    en_names, str_names = cts400_names(en), cts400_names(strings)
    assert en_names, "no cts400_* names in en.json"
    # the two translation files must agree with each other ...
    assert en_names == str_names, en_names ^ str_names
    # ... and every name actually referenced by a platform module must have a
    # translation in BOTH files (catches a name missing from either file).
    referenced = _referenced_cts400_names()
    assert referenced, "no cts400_* names referenced by platform modules"
    missing_en = referenced - en_names
    assert not missing_en, f"missing from en.json: {sorted(missing_en)}"
    missing_str = referenced - str_names
    assert not missing_str, f"missing from strings.json: {sorted(missing_str)}"
