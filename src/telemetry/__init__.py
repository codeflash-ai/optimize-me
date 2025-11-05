from src.telemetry.setup import setup_telemetry
from src.telemetry.decorators import trace_function, trace_function_with_metrics

__all__ = [
    "setup_telemetry",
    "trace_function",
    "trace_function_with_metrics",  # Placeholder for metrics implementation (currently behaves like trace_function)
]

