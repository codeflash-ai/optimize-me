import logging
import sys
from typing import Optional

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from src.telemetry.config import TelemetryConfig

# Note: For true auto-instrumentation, use the `opentelemetry-instrument` command
# This programmatic setup uses individual instrumentors as a fallback

# Library-specific instrumentors (fallback if auto-instrumentation not used)
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
    use_auto_instrumentation: bool = True,
) -> None:
    """Setup OpenTelemetry with auto-instrumentation support.
    
    This function sets up OpenTelemetry using the standard auto-instrumentation
    pattern used by large open-source projects. It supports multiple exporters
    (console, OTLP) and can use auto-instrumentation for libraries.
    
    Args:
        service_name: Name of the service (defaults to config)
        service_version: Version of the service (defaults to config)
        exporter_type: Type of exporter ('console' or 'otlp')
        exporter_endpoint: Endpoint for OTLP exporter
        enabled: Whether telemetry is enabled
        use_auto_instrumentation: Whether to use auto-instrumentation (recommended)
    """
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

    # Check if TracerProvider already exists (e.g., from opentelemetry-instrument)
    existing_provider = trace.get_tracer_provider()
    logger.debug(f"Existing TracerProvider: {type(existing_provider).__name__}, IsNoOp: {isinstance(existing_provider, trace.NoOpTracerProvider)}")
    
    # Handle ProxyTracerProvider (used by opentelemetry-instrument)
    # ProxyTracerProvider doesn't support add_span_processor directly
    # When opentelemetry-instrument is used, we need to create a real TracerProvider
    # to ensure our decorators work correctly
    if existing_provider is not None and not isinstance(existing_provider, trace.NoOpTracerProvider):
        # Check if it's a ProxyTracerProvider
        provider_type_name = type(existing_provider).__name__
        if provider_type_name == "ProxyTracerProvider":
            logger.info("Detected ProxyTracerProvider from opentelemetry-instrument")
            logger.info("Creating new TracerProvider to support span processors")
            # Create a new TracerProvider to replace the proxy
            # This ensures our decorators can create recording spans
            tracer_provider = TracerProvider(resource=resource)
            trace.set_tracer_provider(tracer_provider)
        elif isinstance(existing_provider, TracerProvider):
            logger.info("Using existing TracerProvider")
            tracer_provider = existing_provider
        else:
            logger.info(f"Unknown provider type ({provider_type_name}), creating new TracerProvider")
            tracer_provider = TracerProvider(resource=resource)
            trace.set_tracer_provider(tracer_provider)
        
        # Check existing span processors
        if hasattr(tracer_provider, '_span_processors'):
            logger.debug(f"Existing span processors: {len(tracer_provider._span_processors)}")
            for i, proc in enumerate(tracer_provider._span_processors):
                logger.debug(f"  [{i}] {type(proc).__name__}")
    else:
        logger.info("Creating new TracerProvider")
        tracer_provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(tracer_provider)

    # Setup exporter
    if exporter_type == "console":
        exporter = ConsoleSpanExporter()
        logger.info("Using console exporter for telemetry")
    elif exporter_type == "otlp":
        exporter = OTLPSpanExporter(endpoint=exporter_endpoint)
        logger.info(f"Using OTLP exporter with endpoint: {exporter_endpoint}")
    else:
        exporter = ConsoleSpanExporter()
        logger.warning(f"Unknown exporter type '{exporter_type}', using console")

    # Add span processor (works with existing or new provider)
    # Use SimpleSpanProcessor for console exporter to see traces immediately
    # Use BatchSpanProcessor for OTLP exporter for better performance
    if exporter_type == "console":
        span_processor = SimpleSpanProcessor(exporter)
    else:
        span_processor = BatchSpanProcessor(exporter)
    
    if hasattr(tracer_provider, "add_span_processor"):
        tracer_provider.add_span_processor(span_processor)
        logger.info(f"Added {type(span_processor).__name__} to TracerProvider")
        
        # Verify it was added
        if hasattr(tracer_provider, '_span_processors'):
            logger.debug(f"Total span processors after adding: {len(tracer_provider._span_processors)}")
            for i, proc in enumerate(tracer_provider._span_processors):
                logger.debug(f"  [{i}] {type(proc).__name__}")
    else:
        logger.warning("TracerProvider doesn't support add_span_processor")

    # Note: True auto-instrumentation is best achieved via `opentelemetry-instrument` command
    # This programmatic setup instruments specific libraries (NumPy, Pandas)
    # For full auto-instrumentation, use: opentelemetry-instrument python your_script.py
    if use_auto_instrumentation:
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
        
        logger.info("For full auto-instrumentation, use: opentelemetry-instrument python your_script.py")

    logger.info(f"OpenTelemetry initialized for service: {service_name} v{service_version}")
    
    # Force flush any pending spans (important for console exporter)
    if hasattr(tracer_provider, "force_flush"):
        try:
            tracer_provider.force_flush()
        except Exception as e:
            logger.debug(f"Could not flush tracer provider: {e}")


def get_tracer(name: str):
    return trace.get_tracer(name)

