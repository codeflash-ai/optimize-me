from src.dsa.nodes import find_cycle_vertices, find_node_clusters
from src.dsa.caching_memoization import time_based_cache
import time
import pytest


def test_empty_graph():
    edges = []
    assert find_cycle_vertices(edges) == []


def test_no_cycles_dag():
    edges = [(1, 2), (2, 3), (1, 3)]
    assert find_cycle_vertices(edges) == []


def test_simple_triangle_cycle():
    edges = [(1, 2), (2, 3), (3, 1)]
    assert find_cycle_vertices(edges) == [1, 2, 3]


def test_simple_two_node_cycle():
    edges = [(10, 20), (20, 10)]
    assert find_cycle_vertices(edges) == [10, 20]


def test_self_loop():
    edges = [(1, 1)]
    assert find_cycle_vertices(edges) == [1]


def test_multiple_disjoint_cycles():
    edges = [(1, 2), (2, 1), (3, 4), (4, 5), (5, 3)]
    assert find_cycle_vertices(edges) == [1, 2, 3, 4, 5]


def test_multiple_overlapping_cycles():
    edges = [
        (1, 2),
        (2, 3),
        (3, 1),
        (2, 4),
        (4, 5),
        (5, 2),
    ]
    assert find_cycle_vertices(edges) == [1, 2, 3, 4, 5]


def test_cycle_with_extra_nodes_edges():
    edges = [
        (1, 2),
        (2, 3),
        (3, 1),
        (0, 1),
        (3, 4),
        (5, 6),
    ]
    assert find_cycle_vertices(edges) == [1, 2, 3]


def test_figure_eight():
    edges = [
        (1, 2),
        (2, 3),
        (3, 1),
        (3, 4),
        (4, 5),
        (5, 3),
    ]
    assert find_cycle_vertices(edges) == [1, 2, 3, 4, 5]


def test_complex_graph():
    edges = [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 1),
        (3, 5),
        (5, 6),
        (6, 3),
        (4, 7),
        (8, 1),
        (9, 10),
    ]
    assert find_cycle_vertices(edges) == [1, 2, 3, 4, 5, 6]


def test_string_vertices():
    edges = [
        ("A", "B"),
        ("B", "C"),
        ("C", "A"),
        ("B", "D"),
        ("X", "Y"),
    ]
    assert find_cycle_vertices(edges) == ["A", "B", "C"]


def sort_clusters(clusters):
    """Sorts nodes within each cluster by ID, then sorts clusters by the first node ID."""
    if not clusters:
        return []
    # Sort nodes within each cluster
    sorted_inner = [
        sorted(cluster, key=lambda node: node["id"]) for cluster in clusters
    ]
    # Sort clusters based on the ID of their first node
    sorted_outer = sorted(sorted_inner, key=lambda cluster: cluster[0]["id"])
    return sorted_outer


# --- Test Cases ---


def test_empty_graph():
    """Tests an empty graph with no nodes or edges."""
    nodes = []
    edges = []
    expected = []
    assert sort_clusters(find_node_clusters(nodes, edges)) == sort_clusters(expected)


def test_no_edges():
    """Tests a graph with nodes but no edges. Each node should be its own cluster."""
    nodes = [{"id": 1}, {"id": 2}, {"id": 3}]
    edges = []
    expected = [[{"id": 1}], [{"id": 2}], [{"id": 3}]]
    assert sort_clusters(find_node_clusters(nodes, edges)) == sort_clusters(expected)


def test_single_cluster():
    """Tests a graph where all nodes are connected in one cluster."""
    nodes = [{"id": "A"}, {"id": "B"}, {"id": "C"}, {"id": "D"}]
    edges = [
        {"source": "A", "target": "B"},
        {"source": "B", "target": "C"},
        {"source": "A", "target": "C"},
        {"source": "D", "target": "A"},
    ]
    expected = [[{"id": "A"}, {"id": "B"}, {"id": "C"}, {"id": "D"}]]
    assert sort_clusters(find_node_clusters(nodes, edges)) == sort_clusters(expected)


def test_two_disjoint_clusters():
    """Tests a graph with two separate connected components."""
    nodes = [{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}]
    edges = [
        {"source": 1, "target": 2},  # Cluster 1
        {"source": 3, "target": 4},  # Cluster 2
        {"source": 4, "target": 5},  # Cluster 2
    ]
    expected = [
        [{"id": 1}, {"id": 2}],
        [{"id": 3}, {"id": 4}, {"id": 5}],
    ]
    assert sort_clusters(find_node_clusters(nodes, edges)) == sort_clusters(expected)


def test_isolated_nodes_and_cluster():
    """Tests a graph with a cluster and some nodes not connected to anything."""
    nodes = [{"id": 10}, {"id": 20}, {"id": 30}, {"id": 40}]
    edges = [
        {"source": 10, "target": 20},
    ]
    expected = [
        [{"id": 10}, {"id": 20}],
        [{"id": 30}],
        [{"id": 40}],
    ]
    assert sort_clusters(find_node_clusters(nodes, edges)) == sort_clusters(expected)


def test_node_data_preserved():
    """Tests that the original node dictionary data is preserved in the clusters."""
    nodes = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    edges = [{"source": 1, "target": 2}]
    expected = [[{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]]
    result = find_node_clusters(nodes, edges)
    # Need to sort before checking equality
    assert sort_clusters(result) == sort_clusters(expected)
    # Optional: Check if specific node data is present in the result
    assert any(node.get("name") == "Alice" for cluster in result for node in cluster)
    assert any(node.get("name") == "Bob" for cluster in result for node in cluster)


def test_duplicate_edges():
    """Tests that duplicate edges don't change the clustering outcome."""
    nodes = [{"id": 1}, {"id": 2}, {"id": 3}]
    edges = [
        {"source": 1, "target": 2},
        {"source": 2, "target": 1},
        {"source": 1, "target": 2},
    ]
    expected = [
        [{"id": 1}, {"id": 2}],
        [{"id": 3}],
    ]
    assert sort_clusters(find_node_clusters(nodes, edges)) == sort_clusters(expected)


def test_cycle_in_cluster():
    """Tests that a cycle within a component is handled correctly."""
    nodes = [{"id": 1}, {"id": 2}, {"id": 3}]
    edges = [
        {"source": 1, "target": 2},
        {"source": 2, "target": 3},
        {"source": 3, "target": 1},  # Creates a cycle
    ]
    expected = [[{"id": 1}, {"id": 2}, {"id": 3}]]
    assert sort_clusters(find_node_clusters(nodes, edges)) == sort_clusters(expected)


def test_edge_to_nonexistent_node_causes_error():
    """
    Tests that referencing a node ID in 'edges' that is not present
    in the 'nodes' list raises a KeyError during lookup.
    """
    nodes = [{"id": 1}]
    edges = [{"source": 1, "target": 99}]
    with pytest.raises(KeyError):
        find_node_clusters(nodes, edges)


def test_duplicate_node_ids_last_one_wins():
    nodes = [
        {"id": 1, "value": "first"},
        {"id": 2},
        {"id": 1, "value": "second"},  # This one overwrites the first node with id=1
    ]
    edges = [{"source": 1, "target": 2}]
    expected = [
        [
            {"id": 1, "value": "second"},
            {"id": 2},
        ],  # Expect the 'second' version of node 1
    ]
    result = find_node_clusters(nodes, edges)
    assert sort_clusters(result) == sort_clusters(expected)
    found_node_1 = None
    for cluster in result:
        for node in cluster:
            if node["id"] == 1:
                found_node_1 = node
                break
        if found_node_1:
            break
    assert found_node_1 is not None
    assert found_node_1.get("value") == "second"



call_counter = [0]


def _test_func_simple(a: int, b: int) -> int:
    call_counter[0] += 1
    return a + b


def _test_func_no_args() -> float:
    call_counter[0] += 1
    return time.perf_counter()


def _test_func_kwargs(x: int, y: str = "default") -> str:
    call_counter[0] += 1
    return f"{x}-{y}"


def test_cache_hit():
    call_counter[0] = 0
    cached_func = time_based_cache(expiry_seconds=1)(_test_func_simple)

    result1 = cached_func(1, 2)
    assert result1 == 3
    assert call_counter[0] == 1

    result2 = cached_func(1, 2)
    assert result2 == 3
    assert call_counter[0] == 1

    result3 = cached_func(5, 10)
    assert result3 == 15
    assert call_counter[0] == 2

    result4 = cached_func(5, 10)
    assert result4 == 15
    assert call_counter[0] == 2


def test_cache_expiry():
    call_counter[0] = 0
    expiry_duration = 0.1
    cached_func = time_based_cache(expiry_seconds=expiry_duration)(_test_func_simple)

    result1 = cached_func(10, 20)
    assert result1 == 30
    assert call_counter[0] == 1

    time.sleep(expiry_duration + 0.05)

    result2 = cached_func(10, 20)
    assert result2 == 30
    assert call_counter[0] == 2

    result3 = cached_func(10, 20)
    assert result3 == 30
    assert call_counter[0] == 2


def test_different_arguments():
    call_counter[0] = 0
    cached_func = time_based_cache(expiry_seconds=1)(_test_func_simple)

    res_1_2 = cached_func(1, 2)
    assert res_1_2 == 3
    assert call_counter[0] == 1

    res_3_4 = cached_func(3, 4)
    assert res_3_4 == 7
    assert call_counter[0] == 2

    res_1_2_again = cached_func(1, 2)
    assert res_1_2_again == 3
    assert call_counter[0] == 2

    res_3_4_again = cached_func(3, 4)
    assert res_3_4_again == 7
    assert call_counter[0] == 2


def test_keyword_arguments():
    call_counter[0] = 0
    cached_func = time_based_cache(expiry_seconds=1)(_test_func_kwargs)

    res1 = cached_func(10)
    assert res1 == "10-default"
    assert call_counter[0] == 1

    res2 = cached_func(10)
    assert res2 == "10-default"
    assert call_counter[0] == 1

    res3 = cached_func(x=10, y="default")
    assert res3 == "10-default"
    assert call_counter[0] == 2

    res4 = cached_func(x=10, y="default")
    assert res4 == "10-default"
    assert call_counter[0] == 2

    res5 = cached_func(y="default", x=10)
    assert res5 == "10-default"
    assert call_counter[0] == 2

    res6 = cached_func(x=10, y="explicit")
    assert res6 == "10-explicit"
    assert call_counter[0] == 3

    res7 = cached_func(x=10, y="explicit")
    assert res7 == "10-explicit"
    assert call_counter[0] == 3


def test_no_arguments_function():
    call_counter[0] = 0
    expiry_duration = 0.1
    cached_func = time_based_cache(expiry_seconds=expiry_duration)(_test_func_no_args)

    res1 = cached_func()
    assert call_counter[0] == 1
    time.sleep(0.01)

    res2 = cached_func()
    assert res2 == res1
    assert call_counter[0] == 1

    time.sleep(expiry_duration + 0.05)

    res3 = cached_func()
    assert res3 != res1
    assert call_counter[0] == 2


def test_different_cache_instances():
    call_counter_a = [0]
    call_counter_b = [0]

    def func_a(x):
        call_counter_a[0] += 1
        return x * 2

    def func_b(x):
        call_counter_b[0] += 1
        return x + 10

    cached_a = time_based_cache(expiry_seconds=1)(func_a)
    cached_b = time_based_cache(expiry_seconds=1)(func_b)

    res_a1 = cached_a(5)
    assert res_a1 == 10
    assert call_counter_a[0] == 1
    assert call_counter_b[0] == 0

    res_b1 = cached_b(5)
    assert res_b1 == 15
    assert call_counter_a[0] == 1
    assert call_counter_b[0] == 1

    res_a2 = cached_a(5)
    assert res_a2 == 10
    assert call_counter_a[0] == 1
    assert call_counter_b[0] == 1

    res_b2 = cached_b(5)
    assert res_b2 == 15
    assert call_counter_a[0] == 1
    assert call_counter_b[0] == 1
