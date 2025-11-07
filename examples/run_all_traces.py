"""
Run all instrumented functions and display their trace outputs.

This script demonstrates OpenTelemetry auto-instrumentation.
Functions are automatically instrumented via OpenTelemetry auto-instrumentation
(no decorators needed for libraries like NumPy and Pandas).

Usage:
    # With console exporter (default)
    python examples/run_all_traces.py
    
    # With OTLP exporter (requires docker-compose up)
    # First: cd src/telemetry && docker-compose up -d
    OTEL_TRACES_EXPORTER=otlp OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 python examples/run_all_traces.py
    
    # Or use opentelemetry-instrument command (recommended)
    # Note: Set OTEL_TRACES_EXPORTER=console to see traces in console
    OTEL_TRACES_EXPORTER=console opentelemetry-instrument python examples/run_all_traces.py
"""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import numpy as np
import pandas as pd

from src.telemetry import setup_telemetry
from src.numerical.optimization import gradient_descent
from src.algorithms.graph import graph_traversal, find_node_clusters, PathFinder, calculate_node_betweenness
from src.algorithms.dynamic_programming import fibonacci, matrix_sum, matrix_chain_order, coin_change, knapsack
from src.data_processing.dataframe import dataframe_filter, groupby_mean, dataframe_merge
from src.statistics.descriptive import describe, correlation

# Initialize OpenTelemetry with auto-instrumentation
# Uses environment variables if set, otherwise defaults to console exporter
print("=" * 80)
print("Initializing OpenTelemetry with auto-instrumentation...")
print("=" * 80)

# Enable debug logging if needed
import logging
if os.getenv("OTEL_LOG_LEVEL", "").upper() == "DEBUG":
    logging.basicConfig(level=logging.DEBUG)

# Check if running via opentelemetry-instrument (which sets up OTel automatically)
# opentelemetry-instrument uses OTEL_TRACES_EXPORTER, but we also support OTEL_EXPORTER_TYPE for compatibility
exporter_type = os.getenv("OTEL_TRACES_EXPORTER") or os.getenv("OTEL_EXPORTER_TYPE", "console")
exporter_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")

setup_telemetry(
    service_name="optimize-me",
    service_version="0.1.0",
    exporter_type=exporter_type,
    exporter_endpoint=exporter_endpoint,
    use_auto_instrumentation=True,  # Use auto-instrumentation (standard pattern)
)

print("\n" + "=" * 80)
print("RUNNING ALL INSTRUMENTED FUNCTIONS")
print("=" * 80)
print("\nTraces will appear as JSON objects below each function call.\n")

# ============================================================================
# Numerical Optimization
# ============================================================================
print("\n--- Numerical Optimization ---")
print("Running gradient_descent...")
X = np.array([[1, 2], [3, 4], [5, 6]])
y = np.array([1, 2, 3])
weights = gradient_descent(X, y, learning_rate=0.01, iterations=100)
print(f"Result: {weights}\n")

# ============================================================================
# Graph Algorithms
# ============================================================================
print("\n--- Graph Algorithms ---")

print("Running graph_traversal...")
graph = {1: {2, 3}, 2: {4}, 3: {4}, 4: {}}
visited = graph_traversal(graph, 1)
print(f"Result: {visited}\n")

print("Running find_node_clusters...")
nodes = [{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}]
edges = [{"source": 1, "target": 2}, {"source": 3, "target": 4}]
clusters = find_node_clusters(nodes, edges)
print(f"Result: {clusters}\n")

print("Running PathFinder.find_shortest_path...")
path_finder = PathFinder({"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []})
path = path_finder.find_shortest_path("A", "D")
print(f"Result: {path}\n")

print("Running calculate_node_betweenness...")
nodes_list = ["A", "B", "C", "D"]
edges_list = [{"source": "A", "target": "B"}, {"source": "B", "target": "C"}, {"source": "C", "target": "D"}]
betweenness = calculate_node_betweenness(nodes_list, edges_list)
print(f"Result: {betweenness}\n")

# ============================================================================
# Dynamic Programming
# ============================================================================
print("\n--- Dynamic Programming ---")

print("Running fibonacci...")
fib_result = fibonacci(10)
print(f"Result: {fib_result}\n")

print("Running matrix_sum...")
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
matrix_result = matrix_sum(matrix)
print(f"Result: {matrix_result}\n")

print("Running matrix_chain_order...")
matrices = [(10, 20), (20, 30), (30, 40)]
chain_result = matrix_chain_order(matrices)
print(f"Result: {chain_result}\n")

print("Running coin_change...")
coins = [1, 2, 5]
amount = 5
coin_result = coin_change(coins, amount, 0)
print(f"Result: {coin_result}\n")

print("Running knapsack...")
weights = [10, 20, 30]
values = [60, 100, 120]
capacity = 50
knapsack_result = knapsack(weights, values, capacity, len(weights))
print(f"Result: {knapsack_result}\n")

# ============================================================================
# Data Processing
# ============================================================================
print("\n--- Data Processing ---")

print("Running dataframe_filter...")
df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [10, 20, 30, 40, 50]})
filtered = dataframe_filter(df, "A", 3)
print(f"Result:\n{filtered}\n")

print("Running groupby_mean...")
df_group = pd.DataFrame({
    "group": ["A", "A", "B", "B", "C"],
    "value": [10, 20, 30, 40, 50]
})
grouped = groupby_mean(df_group, "group", "value")
print(f"Result: {grouped}\n")

print("Running dataframe_merge...")
df_left = pd.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"]})
df_right = pd.DataFrame({"id": [2, 3, 4], "age": [25, 30, 35]})
merged = dataframe_merge(df_left, df_right, "id", "id")
print(f"Result:\n{merged}\n")

# ============================================================================
# Statistics
# ============================================================================
print("\n--- Statistics ---")

print("Running describe...")
series = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
stats = describe(series)
print(f"Result: {stats}\n")

print("Running correlation...")
df_corr = pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [2, 4, 6, 8, 10],
    "z": [1, 3, 5, 7, 9]
})
corr_result = correlation(df_corr)
print(f"Result: {corr_result}\n")

print("=" * 80)
print("ALL FUNCTIONS EXECUTED")
print("=" * 80)

if exporter_type == "console":
    print("\n✅ Traces printed to console above (JSON format)")
    print("\nTo view traces in Jaeger UI:")
    print("  1. Start services: cd src/telemetry && docker-compose up -d")
    print("  2. Set environment: export OTEL_TRACES_EXPORTER=otlp")
    print("  3. Run: python examples/run_all_traces.py")
    print("  4. Open: http://localhost:16686")
elif exporter_type == "otlp":
    print(f"\n✅ Traces sent to OTLP endpoint: {exporter_endpoint}")
    print("\nView traces in Jaeger UI: http://localhost:16686")
    print("(Make sure docker-compose is running: cd src/telemetry && docker-compose up -d)")

print("\nOpenTelemetry auto-instrumentation automatically captured:")
print("  - NumPy operations (array operations)")
print("  - Pandas operations (DataFrame operations)")
print("  - Function execution times")
print("  - Service information (service.name, service.version)")
print("\nFor more details, see: src/telemetry/README.md")

# Force flush spans to ensure they're exported (especially for console exporter)
try:
    from opentelemetry import trace
    provider = trace.get_tracer_provider()
    if hasattr(provider, "force_flush"):
        provider.force_flush()
except Exception:
    pass

print()

