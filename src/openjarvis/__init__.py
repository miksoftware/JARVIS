"""MIK-JARVIS — Asistente de Inteligencia Artificial modular desarrollado por MIK Software."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from openjarvis.sdk import Jarvis, JarvisSystem, MemoryHandle, SystemBuilder

try:
    __version__ = _pkg_version("mik-jarvis")
except PackageNotFoundError:  # pragma: no cover — uninstalled source tree
    try:
        __version__ = _pkg_version("openjarvis")
    except PackageNotFoundError:
        __version__ = "1.0.0"

__all__ = ["Jarvis", "JarvisSystem", "MemoryHandle", "SystemBuilder", "__version__"]

_SDK_EXPORTS = {"Jarvis", "JarvisSystem", "MemoryHandle", "SystemBuilder"}


def __getattr__(name: str) -> Any:
    """Load SDK exports lazily so lightweight CLI diagnostics can start safely."""
    if name not in _SDK_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    from openjarvis import sdk

    value = getattr(sdk, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | _SDK_EXPORTS)
