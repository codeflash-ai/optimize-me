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

- Automatically traced using `auto_instrument_package()` or `auto_instrument_modules()`

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

- Automatically traced using `auto_instrument_package()` or `auto_instrument_modules()`

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

| Aspect                    | `opentelemetry-instrument`     | Programmatic Setup             |
| ------------------------- | ------------------------------ | ------------------------------ |
| **Instrumentation Scope** | ALL supported libraries (50+)  | Only NumPy & Pandas            |
| **TracerProvider**        | Created automatically          | Created by `setup_telemetry()` |
| **Setup Location**        | Before script runs             | Inside the script              |
| **Configuration**         | Environment variables          | Function parameters + env vars |
| **Custom Functions**      | Auto-instrumentation available | Auto-instrumentation available |
| **Ease of Use**           | ✅ Zero code changes           | ⚠️ Need to call function       |
| **Flexibility**           | ⚠️ Less control                | ✅ More control                |

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

- ✅ `opentelemetry-instrument` for automatic library instrumentation
- ✅ `auto_instrument_package()` for automatic custom function instrumentation
- ✅ `setup_telemetry()` for custom exporter configuration
- ✅ Best of all worlds! Zero decorators needed!

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

### With `opentelemetry-instrument` + Auto-Instrumentation:

```python
from src.telemetry import setup_telemetry, auto_instrument_package

# Setup OpenTelemetry
setup_telemetry(service_name="my-service", exporter_type="console")

# Enable auto-instrumentation for custom functions (BEFORE imports!)
auto_instrument_package('src', exclude_modules=['src.tests'])

# Import modules - functions are automatically traced
from src.numerical.optimization import gradient_descent
from src.algorithms.graph import graph_traversal

import numpy as np
import pandas as pd
import requests  # Also instrumented!

# All of these generate traces automatically:
np.array([1, 2, 3])           # ✅ Traced (NumPy)
pd.DataFrame(...)             # ✅ Traced (Pandas)
requests.get("http://...")    # ✅ Traced (Requests)
gradient_descent(...)         # ✅ Traced (auto-instrumented custom function)
graph_traversal(...)          # ✅ Traced (auto-instrumented custom function)
```

### With Programmatic Setup Only + Auto-Instrumentation:

```python
from src.telemetry import setup_telemetry, auto_instrument_package

# Setup OpenTelemetry
setup_telemetry(
    service_name="my-service",
    exporter_type="console",
    use_auto_instrumentation=True
)

# Enable auto-instrumentation for custom functions
auto_instrument_package('src', exclude_modules=['src.tests'])

# Import modules
from src.numerical.optimization import gradient_descent
import numpy as np
import pandas as pd
import requests  # NOT instrumented!

# Only these generate traces:
np.array([1, 2, 3])           # ✅ Traced (NumPy)
pd.DataFrame(...)             # ✅ Traced (Pandas)
gradient_descent(...)         # ✅ Traced (auto-instrumented custom function)
requests.get("http://...")    # ❌ NOT traced (Requests not instrumented)
```

---

## Auto-Instrumentation for Custom Functions

Both approaches now support **automatic tracing of custom functions** without decorators!

### How It Works:

```python
from src.telemetry import setup_telemetry, auto_instrument_package

# 1. Setup OpenTelemetry
setup_telemetry(service_name="my-service", exporter_type="console")

# 2. Enable auto-instrumentation BEFORE importing modules
auto_instrument_package(
    'src',  # Package to instrument
    include_private=False,  # Don't trace private functions
    exclude_modules=['src.tests', 'src.telemetry']  # Exclude specific modules
)

# 3. Import modules - functions are automatically wrapped
from src.numerical.optimization import gradient_descent
from src.algorithms.graph import graph_traversal

# All functions are now automatically traced - no decorators needed!
result = gradient_descent(...)  # ✅ Automatically traced
```

### Benefits:

- ✅ **No decorators required** - Clean code without `@trace_function`
- ✅ **Automatic coverage** - All functions in specified modules are traced
- ✅ **Works with both approaches** - Compatible with `opentelemetry-instrument` and programmatic setup
- ✅ **Easy to configure** - Exclude modules, control private functions, etc.

### Span Naming:

Auto-instrumented functions create spans with names like:

- `src.numerical.optimization.gradient_descent`
- `src.algorithms.graph.graph_traversal`
- `src.statistics.descriptive.describe`

---

## Summary

**`opentelemetry-instrument`:**

- Instruments all supported libraries automatically (50+ libraries)
- Zero code changes needed for libraries
- Production-ready
- Works with `setup_telemetry()` (detects existing setup)
- Custom functions can be auto-instrumented with `auto_instrument_package()`

**Programmatic Setup:**

- Instruments only NumPy & Pandas (or specific libraries)
- Requires calling `setup_telemetry()`
- More control, less automation
- Good for libraries/frameworks
- Custom functions can be auto-instrumented with `auto_instrument_package()`

**Best Practice:**

1. Use `opentelemetry-instrument` for automatic library instrumentation
2. Use `auto_instrument_package()` for automatic custom function instrumentation
3. Use `setup_telemetry()` for custom exporter configuration
4. **Result:** Maximum instrumentation with zero decorators needed!
