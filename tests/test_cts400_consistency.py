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
    assert en_names == str_names, en_names ^ str_names
