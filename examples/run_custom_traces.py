"""
Custom script to run specific functions and see their trace outputs.

Modify this script to call any functions you want to trace.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import numpy as np
import pandas as pd

from src.telemetry import setup_telemetry

# Import the functions you want to test
from src.numerical.optimization import gradient_descent
from src.algorithms.graph import graph_traversal
from src.algorithms.dynamic_programming import fibonacci
# Add more imports as needed...

# ============================================================================
# Initialize OpenTelemetry
# ============================================================================
setup_telemetry(
    service_name="optimize-me",
    service_version="0.1.0",
    exporter_type="console",  # Change to "otlp" for production
)

# ============================================================================
# Call your functions here - each will generate a trace span
# ============================================================================

print("Running gradient_descent...")
X = np.array([[1, 2], [3, 4]])
y = np.array([1, 2])
result = gradient_descent(X, y, learning_rate=0.01, iterations=50)
print(f"Result: {result}\n")

print("Running fibonacci...")
fib_result = fibonacci(8)
print(f"Result: {fib_result}\n")

print("Running graph_traversal...")
graph = {1: {2, 3}, 2: {4}, 3: {4}, 4: {}}
visited = graph_traversal(graph, 1)
print(f"Result: {visited}\n")

# Add more function calls here to see their traces...

print("\nDone! Check the JSON trace spans above each function result.")

