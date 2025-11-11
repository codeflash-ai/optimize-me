import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.telemetry import setup_telemetry
from src.numerical.optimization import gradient_descent
from src.algorithms.graph import graph_traversal, find_node_clusters
from src.statistics.descriptive import describe
import numpy as np
import pandas as pd

setup_telemetry(
    service_name="optimize-me",
    service_version="0.1.0",
    exporter_type="console",
)

print("Running gradient descent...")
X = np.array([[1, 2], [3, 4], [5, 6]])
y = np.array([1, 2, 3])
weights = gradient_descent(X, y, learning_rate=0.01, iterations=100)
print(f"Final weights: {weights}\n")

print("Running graph traversal...")
graph = {1: {2, 3}, 2: {4}, 3: {4}, 4: {}}
visited = graph_traversal(graph, 1)
print(f"Visited nodes: {visited}\n")

print("Running statistical describe...")
series = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
stats = describe(series)
print(f"Statistics: {stats}\n")

print("Running node clustering...")
nodes = [{"id": 1}, {"id": 2}, {"id": 3}]
edges = [{"source": 1, "target": 2}]
clusters = find_node_clusters(nodes, edges)
print(f"Clusters: {clusters}\n")

print("Telemetry demonstration complete!")

