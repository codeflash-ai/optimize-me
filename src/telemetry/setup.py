import logging
from typing import Optional

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from src.telemetry.config import TelemetryConfig

try:
    from opentelemetry.instrumentation.numpy import NumPyInstrumentor
except ImportError:
    NumPyInstrumentor = None

try:
    from opentelemetry.instrumentation.pandas import PandasInstrumentor
except ImportError:
    PandasInstrumentor = None

logger = logging.getLogger(__name__)


def setup_telemetry(
    service_name: Optional[str] = None,
    service_version: Optional[str] = None,
    exporter_type: Optional[str] = None,
    exporter_endpoint: Optional[str] = None,
    enabled: Optional[bool] = None,
) -> None:
    enabled = enabled if enabled is not None else TelemetryConfig.enabled
    if not enabled:
        logger.info("Telemetry is disabled")
        return

    service_name = service_name or TelemetryConfig.service_name
    service_version = service_version or TelemetryConfig.service_version
    exporter_type = exporter_type or TelemetryConfig.exporter_type
    exporter_endpoint = exporter_endpoint or TelemetryConfig.exporter_endpoint

    resource = Resource.create(
        {
            SERVICE_NAME: service_name,
            SERVICE_VERSION: service_version,
        }
    )

    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)

    if exporter_type == "console":
        exporter = ConsoleSpanExporter()
        logger.info("Using console exporter for telemetry")
    elif exporter_type == "otlp":
        exporter = OTLPSpanExporter(endpoint=exporter_endpoint)
        logger.info(f"Using OTLP exporter with endpoint: {exporter_endpoint}")
    else:
        exporter = ConsoleSpanExporter()
        logger.warning(f"Unknown exporter type '{exporter_type}', using console")

    span_processor = BatchSpanProcessor(exporter)
    tracer_provider.add_span_processor(span_processor)

    if NumPyInstrumentor is not None:
        try:
            NumPyInstrumentor().instrument()
            logger.info("NumPy instrumentation enabled")
        except Exception as e:
            logger.warning(f"Failed to enable NumPy instrumentation: {e}")
    else:
        logger.debug("NumPy instrumentation not available")

    if PandasInstrumentor is not None:
        try:
            PandasInstrumentor().instrument()
            logger.info("Pandas instrumentation enabled")
        except Exception as e:
            logger.warning(f"Failed to enable Pandas instrumentation: {e}")
    else:
        logger.debug("Pandas instrumentation not available")

    logger.info(f"OpenTelemetry initialized for service: {service_name} v{service_version}")


def get_tracer(name: str):
    return trace.get_tracer(name)

