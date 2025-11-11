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
OTEL_TRACES_EXPORTER=console opentelemetry-instrument python examples/run_all_traces.py

# Or in code
setup_telemetry(exporter_type="console")
```

### Datadog Exporter

Datadog fully supports OpenTelemetry auto-instrumentation! You can use `opentelemetry-instrument` to automatically instrument your application and send traces to Datadog.

**Important:** The Datadog Agent requires an API key even for local usage because it forwards traces to Datadog's cloud service. If you want to test locally without an API key, use **Jaeger** instead (see [OTLP Exporter](#otlp-exporter-production) section).

**Two approaches:**

1. **OTLP (Recommended for auto-instrumentation)** - Use `opentelemetry-instrument` with OTLP exporter pointing to Datadog Agent
2. **Datadog Exporter** - Use the Datadog-specific exporter (works with auto-instrumentation too)

#### Prerequisites

1. **Start Datadog Agent** (if running locally):

   **Option A: Using Docker Compose (Recommended - Easiest)**

   ```bash
   export DD_API_KEY=your-api-key
   export DD_SITE=us5.datadoghq.com  # or datadoghq.com, datadoghq.eu, etc.
   cd src/telemetry
   docker-compose --profile datadog up -d datadog-agent
   ```

   **Option B: Using Docker Run (Manual Setup)**

   ```bash
   # Stop existing dd-agent if running
   docker stop dd-agent 2>/dev/null || true
   docker rm dd-agent 2>/dev/null || true

   # Start with OTLP ports exposed (required for opentelemetry-instrument)
   docker run -d --name datadog-agent \
     -p 8126:8126 \
     -p 4317:4317 \
     -p 4318:4318 \
     -e DD_API_KEY=your-api-key \
     -e DD_SITE=us5.datadoghq.com \
     -e DD_APM_ENABLED=true \
     -e DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC_ENDPOINT=0.0.0.0:4317 \
     -e DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_HTTP_ENDPOINT=0.0.0.0:4318 \
     -v /var/run/docker.sock:/var/run/docker.sock:ro \
     -v /proc/:/host/proc/:ro \
     -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
     datadog/agent:latest
   ```

   **Important:** The Datadog Agent must expose ports **4317** (OTLP gRPC) and **4318** (OTLP HTTP) for `opentelemetry-instrument` to work. The default Datadog setup uses socket-based communication which won't work with OTLP.

#### Usage

**Recommended: Using Docker Compose (Easiest)**

```bash
# 1. Get your API key (see "Getting Your Datadog API Key" section below)
# Then set it:
export DD_API_KEY=your-api-key

# 2. Start Datadog Agent
cd src/telemetry
docker-compose --profile datadog up -d datadog-agent

# 3. Run your application with auto-instrumentation
export DD_SERVICE=optimize-me
export DD_ENV=development

OTEL_TRACES_EXPORTER=otlp \
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 \
opentelemetry-instrument python examples/run_all_traces.py
```

**Option 1: Using opentelemetry-instrument with OTLP (Recommended for Auto-Instrumentation)**

This is the **best approach for auto-instrumentation** because:

- ✅ Full auto-instrumentation of all supported libraries
- ✅ Standard OpenTelemetry approach
- ✅ Works seamlessly with Datadog Agent (7.17+)
- ✅ No code changes needed

```bash
# Set environment variables
export DD_API_KEY=your-api-key
export DD_SITE=datadoghq.com  # or datadoghq.eu for EU
export DD_ENV=production  # Optional
export DD_SERVICE=optimize-me  # Optional
export DD_VERSION=0.1.0  # Optional

# Configure Datadog Agent to accept OTLP (default in Agent 7.17+)
# Agent listens on port 4317 for OTLP gRPC

# Run with auto-instrumentation and OTLP exporter
OTEL_TRACES_EXPORTER=otlp \
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 \
opentelemetry-instrument python examples/run_all_traces.py
```

**Note:** Datadog Agent 7.17+ natively supports OTLP on port 4317, so you can use the standard OTLP exporter. This gives you full auto-instrumentation benefits while sending traces to Datadog.

**Option 2: Using Programmatic Setup with Datadog Exporter**

This approach uses the Datadog-specific exporter. It still works with auto-instrumentation if you use `opentelemetry-instrument`:

```bash
# Install Datadog exporter
pip install opentelemetry-exporter-datadog

# Set environment variables
export DD_API_KEY=your-api-key
export DD_AGENT_URL=http://localhost:8126
export DD_ENV=production

# Use opentelemetry-instrument for auto-instrumentation
# Your code will use the Datadog exporter
opentelemetry-instrument python examples/run_all_traces.py
```

Or in your code:

```python
from src.telemetry import setup_telemetry

setup_telemetry(
    service_name="optimize-me",
    service_version="0.1.0",
    exporter_type="datadog",  # Uses Datadog-specific exporter
    use_auto_instrumentation=True,
)
```

**Option 3: Direct Datadog Exporter (Advanced)**

```python
from opentelemetry.exporter.datadog import DatadogSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

# Setup TracerProvider
trace.set_tracer_provider(TracerProvider())

# Add Datadog exporter
datadog_exporter = DatadogSpanExporter(
    agent_url="http://localhost:8126",
    service="optimize-me",
    env="production",
    version="0.1.0",
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(datadog_exporter)
)
```

#### Getting Your Datadog API Key

1. **Sign in to Datadog:**

   - Go to [app.datadoghq.com](https://app.datadoghq.com)
   - If you don't have an account, sign up for a free trial

2. **Navigate to API Keys:**

   - Go to **Organization Settings** → **API Keys**
   - Or visit directly: [https://app.datadoghq.com/organization-settings/api-keys](https://app.datadoghq.com/organization-settings/api-keys)

3. **Create a new API key:**

   - Click **"New Key"** or **"Create Key"**
   - Enter a name (e.g., "Local Development" or "Optimize-Me Project")
   - Click **"Create Key"**

4. **Copy the API key:**

   - **Important:** Copy the key immediately - you won't be able to see it again!
   - The key will look like: `1234567890abcdef1234567890abcdef`

5. **Set it as an environment variable:**
   ```bash
   export DD_API_KEY=your-copied-api-key-here
   ```

**Note:**

- API keys are organization-level credentials
- Keep your API key secure and don't commit it to version control
- You can create multiple API keys for different environments/projects
- To revoke a key, go back to the API Keys page and delete it

#### Environment Variables

**For Docker Compose:**

```bash
# Required: Set before starting docker-compose
# Get your key from: https://app.datadoghq.com/organization-settings/api-keys
export DD_API_KEY=your-api-key

# Optional: Datadog site (default: datadoghq.com)
export DD_SITE=datadoghq.com  # or datadoghq.eu, us3.datadoghq.com, etc.
```

**For Your Application:**

```bash
# Required for Datadog
export DD_API_KEY=your-api-key

# Optional: Service metadata
export DD_SERVICE=optimize-me      # Service name (defaults to OTEL_SERVICE_NAME)
export DD_ENV=development          # Environment (default: "development")
export DD_VERSION=0.1.0            # Service version (defaults to OTEL_SERVICE_VERSION)
export DD_SITE=datadoghq.com       # Datadog site (default: "datadoghq.com")

# For local development with Docker Compose
# Agent URL is automatically http://localhost:4317 (OTLP) or http://localhost:8126 (native)
```

**Note:** When using Docker Compose, the Datadog Agent is configured to accept OTLP on port 4317, so you don't need to set `DD_AGENT_URL`.

#### Auto-Instrumentation with Datadog

**Best Practice:** Use `opentelemetry-instrument` with OTLP exporter for maximum auto-instrumentation:

```bash
# Full auto-instrumentation + Datadog
export DD_API_KEY=your-api-key
export DD_SERVICE=optimize-me
export DD_ENV=production

OTEL_TRACES_EXPORTER=otlp \
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 \
opentelemetry-instrument python your_script.py
```

This automatically instruments:

- ✅ NumPy, Pandas, Requests, SQLAlchemy, Flask, Django, etc.
- ✅ All OpenTelemetry-supported libraries
- ✅ Sends traces to Datadog via OTLP
- ✅ No code changes required

#### Viewing Traces in Datadog

**Important:** Make sure the Datadog Agent is running and has OTLP ports exposed before sending traces!

1. **Verify Datadog Agent is running and receiving traces:**

   ```bash
   # Check container is running
   docker ps | grep datadog-agent

   # Check logs for OTLP receiver messages
   docker logs datadog-agent --tail 50 | grep -i otlp
   # Should see messages like: "OTLP receiver started" or "Listening on 0.0.0.0:4317"

   # Check for trace reception
   docker logs datadog-agent --tail 50 | grep -i trace
   ```

2. **View traces in Datadog:**

   - Go to **Datadog APM** → **Traces** (https://app.datadoghq.com/apm/traces)
   - Filter by service: `optimize-me` (or your `DD_SERVICE` value)
   - Traces may take **1-2 minutes** to appear after sending
   - View trace details, spans, and performance metrics
   - See auto-instrumented spans from all libraries

3. **Troubleshooting if traces don't appear:**
   - **Check API key:** Verify `DD_API_KEY` is set correctly in the container
   - **Check site:** Make sure `DD_SITE` matches your Datadog account (e.g., `us5.datadoghq.com`)
   - **Check ports:** Verify ports 4317/4318 are exposed: `docker port datadog-agent`
   - **Check connection:** Test OTLP endpoint: `curl http://localhost:4318/v1/traces` (should return 405 Method Not Allowed, not Connection Refused)
   - **Check logs:** Look for errors in `docker logs datadog-agent`

### OTLP Exporter (Production)

The OTLP exporter sends traces to an OpenTelemetry Collector or compatible backend (Jaeger, Datadog Agent, etc.).

**For Local Testing Without API Keys:** Use Jaeger - it runs completely locally and doesn't require any API keys or cloud accounts.

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
OTEL_TRACES_EXPORTER=otlp \
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 \
opentelemetry-instrument python examples/run_all_traces.py

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

The project includes a Docker Compose setup for running telemetry backends locally:

### Quick Start

```bash
# Navigate to telemetry directory
cd src/telemetry

# Start Jaeger (for development/testing)
docker-compose up -d jaeger

# Start Datadog Agent (requires DD_API_KEY)
export DD_API_KEY=your-api-key
docker-compose --profile datadog up -d datadog-agent

# View logs
docker-compose logs -f jaeger
docker-compose logs -f datadog-agent

# Stop services
docker-compose down
```

### Services

- **Jaeger** (`http://localhost:16686`) - **Recommended for Local Testing**

  - Built-in OTLP receiver on ports 4317 (gRPC) and 4318 (HTTP)
  - Visualize and search traces
  - Service dependency graphs
  - Trace timeline visualization
  - **No API key required** - runs completely locally
  - **Start:** `docker-compose up -d jaeger`
  - **Best for:** Local development and testing without cloud dependencies

- **Datadog Agent** (requires `DD_API_KEY`)
  - OTLP receiver on ports 4317 (gRPC) and 4318 (HTTP)
  - Native trace endpoint on port 8126
  - **Forwards traces to Datadog APM cloud service** (requires API key)
  - **Start:** `export DD_API_KEY=your-key && docker-compose --profile datadog up -d datadog-agent`
  - **View traces:** Datadog APM → Traces (cloud service)
  - **Best for:** Testing Datadog integration or sending traces to Datadog cloud

**Note:**

- **For local-only testing without API keys:** Use Jaeger - it's completely local and free
- Datadog Agent uses a Docker Compose profile (`datadog`) so it only starts when explicitly requested
- Set `DD_API_KEY` environment variable before starting the Datadog Agent
- **The Datadog Agent forwards traces to Datadog's cloud, so you need an API key even for "local" usage**
- For advanced use cases (processing, routing to multiple backends), you can uncomment the `otel-collector` service in `docker-compose.yml`

## Multiple Exporters

You can configure multiple exporters simultaneously. For example, send traces to both Datadog and OTLP:

```python
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.datadog import DatadogSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry import trace

# Setup base telemetry
setup_telemetry(exporter_type="otlp", exporter_endpoint="http://localhost:4317")

# Add additional exporter
provider = trace.get_tracer_provider()
datadog_exporter = DatadogSpanExporter(
    agent_url="http://localhost:8126",
    service="optimize-me",
    env="production",
)
provider.add_span_processor(BatchSpanProcessor(datadog_exporter))
```

**Note:** You can also use `setup_telemetry(exporter_type="datadog")` to use Datadog as the primary exporter.

## Custom Instrumentation

While auto-instrumentation handles libraries, you can still add custom instrumentation for your application code:

```python
from src.telemetry import auto_instrument_package

# Enable auto-instrumentation BEFORE importing your modules
auto_instrument_package('src', exclude_modules=['src.tests'])

# Import modules - functions are automatically traced
from src.my_module import my_function

# Function is automatically traced - no decorator needed!
my_function(param1=1, param2="test")
```

**Note:** Auto-instrumentation automatically traces all functions in specified modules. No decorators needed!

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

### Example 2: Development (Jaeger via Docker) - **No API Key Required**

```bash
# Terminal 1: Start services (no API key needed!)
cd src/telemetry
docker-compose up -d jaeger

# Terminal 2: Run application
OTEL_TRACES_EXPORTER=otlp \
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 \
opentelemetry-instrument python examples/run_all_traces.py

# View in browser: http://localhost:16686
# All traces are stored locally - no cloud, no API key needed!
```

### Example 3: Local Development with Datadog (Docker Compose)

```bash
# 1. Get and set your Datadog API key
# Get it from: https://app.datadoghq.com/organization-settings/api-keys
export DD_API_KEY=your-api-key

# 2. Start Datadog Agent locally
cd src/telemetry
docker-compose --profile datadog up -d datadog-agent

# 3. Set service metadata
export DD_SERVICE=optimize-me
export DD_ENV=development
export DD_VERSION=0.1.0

# 4. Run with auto-instrumentation
OTEL_TRACES_EXPORTER=otlp \
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 \
opentelemetry-instrument python examples/run_all_traces.py

# 5. View traces in Datadog APM
```

**Alternative:** Using Datadog-specific exporter:

```bash
# Install Datadog exporter
pip install opentelemetry-exporter-datadog

# Start Datadog Agent
export DD_API_KEY=your-api-key
cd src/telemetry
docker-compose --profile datadog up -d datadog-agent

# Set environment variables
export DD_SERVICE=optimize-me
export DD_ENV=development

# Use opentelemetry-instrument for auto-instrumentation
# Your code uses setup_telemetry(exporter_type="datadog")
opentelemetry-instrument python examples/run_all_traces.py
```

### Example 3b: Production with Datadog (Remote Agent)

```bash
# Set Datadog configuration
export DD_API_KEY=your-api-key
export DD_SITE=datadoghq.com
export DD_ENV=production
export DD_SERVICE=optimize-me
export DD_VERSION=0.1.0

# Use opentelemetry-instrument for full auto-instrumentation
# Point to your production Datadog Agent
OTEL_TRACES_EXPORTER=otlp \
OTEL_EXPORTER_OTLP_ENDPOINT=http://your-datadog-agent:4317 \
opentelemetry-instrument python your_production_script.py
```

### Example 4: Production with OTLP Collector

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
