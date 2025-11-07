# OpenTelemetry Setup Guide

This guide explains how to use OpenTelemetry with the `optimize-me` project using the standard auto-instrumentation pattern used by large open-source projects.

## Overview

The project uses **OpenTelemetry auto-instrumentation**, which automatically instruments supported libraries (NumPy, Pandas, etc.) without requiring code changes. This is the same pattern used by production applications in large open-source projects.

## Quick Start

### 1. Using Auto-Instrumentation (Recommended)

The easiest way to use OpenTelemetry is via the `opentelemetry-instrument` command:

```bash
# Install opentelemetry-instrument (if not already installed)
pip install opentelemetry-instrumentation

# Run script with auto-instrumentation and console exporter
OTEL_TRACES_EXPORTER=console opentelemetry-instrument python examples/run_all_traces.py

# For debugging (with verbose logging)
OTEL_LOG_LEVEL=DEBUG OTEL_TRACES_EXPORTER=console opentelemetry-instrument python examples/run_all_traces.py

# Or for OTLP exporter (requires Jaeger running)
OTEL_TRACES_EXPORTER=otlp opentelemetry-instrument python examples/run_all_traces.py
```

This automatically instruments **ALL supported libraries** (NumPy, Pandas, Requests, SQLAlchemy, etc.) and sends traces to the configured exporter.

**What happens:**

- `opentelemetry-instrument` wraps the script and instruments everything automatically
- If the script calls `setup_telemetry()`, it detects the existing setup and adds custom exporters
- **Result:** Maximum instrumentation with custom configuration!

**Note:** When using `opentelemetry-instrument`, set `OTEL_TRACES_EXPORTER=console` to see traces in the console, or `OTEL_TRACES_EXPORTER=otlp` to send to an OTLP endpoint. This is the standard OpenTelemetry environment variable name.

### 2. Using Programmatic Setup

Alternatively, you can use the programmatic setup in your code:

```python
from src.telemetry import setup_telemetry

# Initialize with console exporter
setup_telemetry(
    service_name="optimize-me",
    service_version="0.1.0",
    exporter_type="console",
    use_auto_instrumentation=True,  # Instruments NumPy & Pandas only
)
```

**What happens:**

- `setup_telemetry()` creates a new TracerProvider
- Instruments **only NumPy and Pandas** (not other libraries)
- Adds your custom exporter
- **Note:** For full auto-instrumentation, use `opentelemetry-instrument` command

### Understanding the Difference

For a detailed comparison of `opentelemetry-instrument` vs programmatic setup, see [INSTRUMENTATION_COMPARISON.md](INSTRUMENTATION_COMPARISON.md).

## Exporters

### Console Exporter (Default)

The console exporter prints traces to stdout. This is useful for development and debugging.

```bash
# Using opentelemetry-instrument
opentelemetry-instrument \
  --exporter=console \
  python examples/run_all_traces.py

# Or in code
setup_telemetry(exporter_type="console")
```

### OTLP Exporter (Production)

The OTLP exporter sends traces to an OpenTelemetry Collector or compatible backend (Datadog, Jaeger, etc.).

#### Option 1: Using Docker (Simplest)

1. **Start Jaeger (includes built-in OTLP receiver):**

```bash
# Navigate to telemetry directory
cd src/telemetry

# Start Jaeger
docker-compose up -d

# Check it's running
docker-compose ps

# View logs
docker-compose logs -f jaeger
```

2. **Run your application:**

```bash
# Using opentelemetry-instrument (recommended)
opentelemetry-instrument \
  --exporter=otlp \
  --endpoint=http://localhost:4317 \
  python examples/run_all_traces.py

# Or set environment variables
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
export OTEL_EXPORTER_TYPE=otlp
opentelemetry-instrument python examples/run_all_traces.py

# Or use programmatic setup
OTEL_EXPORTER_TYPE=otlp OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 \
  python examples/run_all_traces.py
```

3. **View traces in Jaeger:**

Open **http://localhost:16686** in your browser to view traces.

- Select service: `optimize-me`
- Click "Find Traces"
- Click on a trace to see details

#### Option 2: Programmatic Setup

```python
from src.telemetry import setup_telemetry

setup_telemetry(
    service_name="optimize-me",
    service_version="0.1.0",
    exporter_type="otlp",
    exporter_endpoint="http://localhost:4317",
    use_auto_instrumentation=True,
)
```

## Environment Variables

You can configure OpenTelemetry using environment variables (standard OpenTelemetry convention):

```bash
# Service information
export OTEL_SERVICE_NAME=optimize-me
export OTEL_SERVICE_VERSION=0.1.0

# Exporter configuration
export OTEL_EXPORTER_TYPE=otlp
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Disable telemetry
export OTEL_SDK_DISABLED=true

# Sampling
export OTEL_TRACES_SAMPLER=always_on
export OTEL_TRACES_SAMPLER_ARG=1.0
```

## Docker Setup

The project includes a Docker Compose setup for running Jaeger (which has built-in OTLP support):

```bash
# Navigate to telemetry directory
cd src/telemetry

# Start Jaeger
docker-compose up -d

# View logs
docker-compose logs -f jaeger

# Stop services
docker-compose down
```

### Services

- **Jaeger** (`http://localhost:16686`)
  - Built-in OTLP receiver on ports 4317 (gRPC) and 4318 (HTTP)
  - Visualize and search traces
  - Service dependency graphs
  - Trace timeline visualization

**Note:** For advanced use cases (processing, routing to multiple backends), you can uncomment the `otel-collector` service in `docker-compose.yml`.

## Multiple Exporters

You can configure multiple exporters simultaneously. For example, send traces to both Datadog and OTLP:

```python
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry import trace

# Setup base telemetry
setup_telemetry(exporter_type="otlp", exporter_endpoint="http://localhost:4317")

# Add additional exporter
provider = trace.get_tracer_provider()
datadog_exporter = DatadogSpanExporter(...)  # Requires opentelemetry-exporter-datadog
provider.add_span_processor(BatchSpanProcessor(datadog_exporter))
```

## Custom Instrumentation

While auto-instrumentation handles libraries, you can still add custom instrumentation for your application code:

```python
from src.telemetry.decorators import trace_function

@trace_function(span_name="my_function", capture_args=["param1"])
def my_function(param1: int, param2: str):
    # Your code here
    pass
```

**Note:** For most use cases, auto-instrumentation is sufficient. Custom decorators are only needed for application-specific tracing.

## Supported Libraries

Auto-instrumentation supports many libraries automatically:

- **NumPy** - Array operations
- **Pandas** - DataFrame operations
- **Requests** - HTTP requests
- **SQLAlchemy** - Database queries
- **Flask/Django** - Web frameworks
- And many more...

See the [OpenTelemetry Python documentation](https://opentelemetry.io/docs/languages/python/instrumentation/) for the full list.

## Troubleshooting

### Traces not appearing

1. **Check exporter endpoint:**

   ```bash
   # Test OTLP endpoint
   curl http://localhost:4318/v1/traces
   ```

2. **Check Docker services:**

   ```bash
   cd src/telemetry
   docker-compose ps
   docker-compose logs jaeger
   ```

3. **Enable debug logging:**

   ```bash
   # With console exporter (see traces in console)
   OTEL_LOG_LEVEL=DEBUG OTEL_TRACES_EXPORTER=console opentelemetry-instrument python examples/run_all_traces.py

   # Or export environment variables first
   export OTEL_LOG_LEVEL=DEBUG
   export OTEL_TRACES_EXPORTER=console
   opentelemetry-instrument python your_script.py
   ```

### Performance impact

Auto-instrumentation has minimal overhead. If needed, you can:

- Use sampling: `export OTEL_TRACES_SAMPLER_ARG=0.1` (10% sampling)
- Disable specific instrumentations: `export OTEL_PYTHON_DISABLED_INSTRUMENTATIONS=requests`

## Best Practices

1. **Use auto-instrumentation** - It's the standard pattern and requires no code changes
2. **Use environment variables** - Makes configuration flexible across environments
3. **Use OTLP exporter in production** - Send to a collector, not directly to backends
4. **Use sampling in production** - Reduce overhead with sampling (e.g., 10% of traces)
5. **Monitor performance** - Auto-instrumentation has minimal overhead, but monitor in production

## Examples

### Example 1: Development (Console)

```bash
# Basic console output
OTEL_TRACES_EXPORTER=console opentelemetry-instrument python examples/run_all_traces.py

# With debug logging (for troubleshooting)
OTEL_LOG_LEVEL=DEBUG OTEL_TRACES_EXPORTER=console opentelemetry-instrument python examples/run_all_traces.py
```

### Example 2: Development (Jaeger via Docker)

```bash
# Terminal 1: Start services
cd src/telemetry
docker-compose up -d

# Terminal 2: Run application
opentelemetry-instrument \
  --exporter=otlp \
  --endpoint=http://localhost:4317 \
  python examples/run_all_traces.py

# View in browser: http://localhost:16686
```

### Example 3: Production (Environment Variables)

```bash
export OTEL_SERVICE_NAME=optimize-me
export OTEL_EXPORTER_TYPE=otlp
export OTEL_EXPORTER_OTLP_ENDPOINT=https://your-collector.example.com:4317
export OTEL_TRACES_SAMPLER_ARG=0.1  # 10% sampling

opentelemetry-instrument python your_production_script.py
```

## Additional Resources

- [OpenTelemetry Python Documentation](https://opentelemetry.io/docs/languages/python/)
- [OpenTelemetry Collector Documentation](https://opentelemetry.io/docs/collector/)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)
