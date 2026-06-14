"""Ensure the repository root is importable so tests can do
`from custom_components.nilan...` without installing the package.

pytest imports this conftest from the repository root and, in the default
"prepend" import mode, inserts this directory onto sys.path.
"""
