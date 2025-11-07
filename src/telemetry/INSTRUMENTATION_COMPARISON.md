# OpenTelemetry Instrumentation: `opentelemetry-instrument` vs Programmatic Setup

This document explains the difference between using the `opentelemetry-instrument` command and the programmatic `setup_telemetry()` function.

## Overview

Both approaches set up OpenTelemetry, but they work differently:

- **`opentelemetry-instrument`**: Wraps the Python script and automatically instruments ALL supported libraries
- **Programmatic Setup**: The application calls `setup_telemetry()` in code, which instruments SPECIFIC libraries (NumPy, Pandas)

## Scenario 1: Using `opentelemetry-instrument` Command

### What Happens:

```bash
opentelemetry-instrument python examples/run_all_traces.py
```

### Step-by-Step Execution:

1. **`opentelemetry-instrument` wrapper activates:**

   - Automatically detects ALL installed OpenTelemetry instrumentation packages
   - Instruments ALL supported libraries (NumPy, Pandas, Requests, SQLAlchemy, etc.)
   - Sets up a default TracerProvider
   - Configures exporters based on environment variables (e.g., `OTEL_TRACES_EXPORTER=console` or `OTEL_TRACES_EXPORTER=otlp`)

2. **The script runs:**

   ```python
   # When the script calls:
   from src.telemetry import setup_telemetry
   setup_telemetry(...)
   ```

3. **`setup_telemetry()` detects existing setup:**
   - Line 69-73: Checks if TracerProvider already exists
   - **Finds existing TracerProvider** (created by `opentelemetry-instrument`)
   - **Uses the existing one** instead of creating a new one
   - Adds custom exporters (console/OTLP) to the existing provider
   - **Skips instrumenting NumPy/Pandas** (already instrumented by `opentelemetry-instrument`)

### What Gets Instrumented:

✅ **ALL supported libraries automatically:**

- NumPy (if installed)
- Pandas (if installed)
- Requests (if installed)
- SQLAlchemy (if installed)
- Flask/Django (if installed)
- And 50+ other libraries

✅ **Custom application functions:**

- Only if using the `@trace_function` decorator

### Example Output:

```
# opentelemetry-instrument automatically instruments everything
# setup_telemetry() detects existing setup and adds exporter
INFO: Using existing OpenTelemetry TracerProvider (likely from opentelemetry-instrument)
INFO: Added span processor to TracerProvider
INFO: OpenTelemetry initialized for service: optimize-me v0.1.0
```

---

## Scenario 2: Using Programmatic Setup Only

### What Happens:

```bash
python examples/run_all_traces.py
```

### Step-by-Step Execution:

1. **The script runs directly:**

   - No automatic instrumentation
   - No TracerProvider exists yet

2. **The script calls `setup_telemetry()`:**

   ```python
   setup_telemetry(
       service_name="optimize-me",
       service_version="0.1.0",
       exporter_type="console",
       use_auto_instrumentation=True,
   )
   ```

3. **`setup_telemetry()` creates new setup:**
   - Line 69-73: Checks for existing TracerProvider
   - **No existing provider found**
   - Line 75-76: Creates NEW TracerProvider
   - Line 90-93: Adds exporters (console/OTLP)
   - Line 98-117: Instruments SPECIFIC libraries:
     - NumPy (if `NumPyInstrumentor` available)
     - Pandas (if `PandasInstrumentor` available)
   - **Does NOT instrument other libraries** (Requests, SQLAlchemy, etc.)

### What Gets Instrumented:

✅ **Only specific libraries:**

- NumPy (manually instrumented)
- Pandas (manually instrumented)

❌ **NOT instrumented:**

- Requests
- SQLAlchemy
- Flask/Django
- Other libraries

✅ **Custom application functions:**

- Only if using the `@trace_function` decorator

### Example Output:

```
# setup_telemetry() creates new TracerProvider
INFO: Using console exporter for telemetry
INFO: Added span processor to TracerProvider
INFO: NumPy instrumentation enabled
INFO: Pandas instrumentation enabled
INFO: For full auto-instrumentation, use: opentelemetry-instrument python your_script.py
INFO: OpenTelemetry initialized for service: optimize-me v0.1.0
```

---

## Key Differences

| Aspect                    | `opentelemetry-instrument`    | Programmatic Setup             |
| ------------------------- | ----------------------------- | ------------------------------ |
| **Instrumentation Scope** | ALL supported libraries (50+) | Only NumPy & Pandas            |
| **TracerProvider**        | Created automatically         | Created by `setup_telemetry()` |
| **Setup Location**        | Before script runs            | Inside the script              |
| **Configuration**         | Environment variables         | Function parameters + env vars |
| **Custom Functions**      | Requires decorators           | Requires decorators            |
| **Ease of Use**           | ✅ Zero code changes          | ⚠️ Need to call function       |
| **Flexibility**           | ⚠️ Less control               | ✅ More control                |

---

## What Happens When Both Are Used?

### Scenario: `opentelemetry-instrument` + `setup_telemetry()`

```bash
opentelemetry-instrument python examples/run_all_traces.py
```

**Execution Flow:**

1. `opentelemetry-instrument` instruments everything
2. `setup_telemetry()` detects existing TracerProvider
3. `setup_telemetry()` adds custom exporters to existing provider
4. **Result:** Best of both worlds!
   - All libraries instrumented (from `opentelemetry-instrument`)
   - Custom exporters configured (from `setup_telemetry()`)

**This is the RECOMMENDED approach!**

---

## When to Use Each

### Use `opentelemetry-instrument` when:

- ✅ Maximum instrumentation is required (all libraries)
- ✅ Zero code changes are desired
- ✅ Running scripts or commands
- ✅ Production-ready setup is needed

### Use Programmatic Setup when:

- ✅ Fine-grained control is required
- ✅ Building a library or framework
- ✅ Only specific libraries need instrumentation
- ✅ Custom configuration logic is needed

### Use Both (Recommended):

- ✅ `opentelemetry-instrument` for automatic instrumentation
- ✅ `setup_telemetry()` for custom exporter configuration
- ✅ Best of both worlds!

---

## Code Flow Diagrams

### Flow 1: `opentelemetry-instrument` Only

```
opentelemetry-instrument python script.py
    ↓
[Wrapper activates]
    ↓
[Instruments ALL libraries]
    ↓
[Creates TracerProvider]
    ↓
[Script runs]
    ↓
setup_telemetry() called
    ↓
[Detects existing TracerProvider] ✅
    ↓
[Adds custom exporters]
    ↓
[Script continues]
```

### Flow 2: Programmatic Setup Only

```
python script.py
    ↓
[Script runs]
    ↓
setup_telemetry() called
    ↓
[No TracerProvider exists] ❌
    ↓
[Creates NEW TracerProvider]
    ↓
[Instruments NumPy & Pandas only]
    ↓
[Adds custom exporters]
    ↓
[Script continues]
```

---

## Example: What Traces Are Generated

### With `opentelemetry-instrument`:

```python
import numpy as np
import pandas as pd
import requests  # Also instrumented!

# All of these generate traces automatically:
np.array([1, 2, 3])           # ✅ Traced
pd.DataFrame(...)             # ✅ Traced
requests.get("http://...")    # ✅ Traced (not with programmatic only!)
```

### With Programmatic Setup Only:

```python
import numpy as np
import pandas as pd
import requests  # NOT instrumented!

# Only these generate traces:
np.array([1, 2, 3])           # ✅ Traced
pd.DataFrame(...)             # ✅ Traced
requests.get("http://...")    # ❌ NOT traced
```

---

## Summary

**`opentelemetry-instrument`:**

- Instruments everything automatically
- Zero code changes needed
- Production-ready
- Works with `setup_telemetry()` (detects existing setup)

**Programmatic Setup:**

- Instruments only NumPy & Pandas
- Requires calling `setup_telemetry()`
- More control, less automation
- Good for libraries/frameworks

**Best Practice:**
Use `opentelemetry-instrument` + `setup_telemetry()` together for maximum instrumentation with custom configuration.
