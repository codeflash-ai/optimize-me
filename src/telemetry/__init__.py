from src.telemetry.setup import setup_telemetry
from src.telemetry.auto_instrumentation import (
    auto_instrument_package,
    auto_instrument_modules,
    auto_instrument_current_package,
)

__all__ = [
    "setup_telemetry",
    "auto_instrument_package",
    "auto_instrument_modules",
    "auto_instrument_current_package",
]

