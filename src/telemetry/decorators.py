import functools
import logging
from typing import Any, Callable, Optional

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

from src.telemetry.config import TelemetryConfig

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


def trace_function(
    func: Optional[Callable] = None,
    *,
    span_name: Optional[str] = None,
    capture_args: Optional[list[str]] = None,
    capture_return: bool = False,
) -> Callable:
    def decorator(f: Callable) -> Callable:
        if not TelemetryConfig.enabled:
            return f

        name = span_name or f"{f.__module__}.{f.__name__}"

        @functools.wraps(f)
        def wrapper(*args, **kwargs) -> Any:
            with tracer.start_as_current_span(name) as span:
                try:
                    if capture_args:
                        import inspect

                        sig = inspect.signature(f)
                        bound = sig.bind(*args, **kwargs)
                        bound.apply_defaults()

                        for arg_name in capture_args:
                            if arg_name in bound.arguments:
                                value = bound.arguments[arg_name]
                                attr_value = str(value)
                                if len(attr_value) > 250:
                                    attr_value = attr_value[:250] + "..."
                                span.set_attribute(f"function.{arg_name}", attr_value)

                    result = f(*args, **kwargs)

                    if capture_return:
                        return_str = str(result)
                        if len(return_str) > 250:
                            return_str = return_str[:250] + "..."
                        span.set_attribute("function.return", return_str)

                    span.set_status(Status(StatusCode.OK))
                    return result

                except Exception as e:
                    span.record_exception(e)
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    logger.error(
                        f"Error in {name}: {e}",
                        exc_info=True,
                        extra={
                            "file": f.__module__,
                            "function": f.__name__,
                            "error": str(e),
                        },
                    )
                    raise

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)

# Placeholder for metrics implementation (currently behaves like trace_function)
def trace_function_with_metrics(
    func: Optional[Callable] = None,
    *,
    span_name: Optional[str] = None,
    capture_args: Optional[list[str]] = None,
) -> Callable:
    return trace_function(
        func,
        span_name=span_name,
        capture_args=capture_args,
        capture_return=False,
    )

