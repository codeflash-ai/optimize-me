/**
 * Graph/Node Operations
 * JavaScript equivalents of Python implementations
 */

/**
 * Find the last (terminal) node in a flow
 * @param {string[]} nodes - Array of node identifiers
 * @param {Array<[string, string]>} edges - Array of [source, target] edges
 * @returns {string|null} - Terminal node or null if not found
 */
export function findLastNode(nodes, edges) {
  const nodesWithOutgoing = new Set(edges.map(([source]) => source));

  for (const node of nodes) {
    if (!nodesWithOutgoing.has(node)) {
      // Verify node has at least one incoming edge or is the only node
      const hasIncoming = edges.some(([, target]) => target === node);
      if (hasIncoming || nodes.length === 1) {
        return node;
      }
    }
  }

  return nodes.length > 0 ? nodes[nodes.length - 1] : null;
}

/**
 * Find all leaf nodes (nodes with no outgoing edges)
 * @param {string[]} nodes - Array of node identifiers
 * @param {Array<[string, string]>} edges - Array of [source, target] edges
 * @returns {string[]} - Array of leaf nodes
 */
export function findLeafNodes(nodes, edges) {
  const nodesWithOutgoing = new Set(edges.map(([source]) => source));
  return nodes.filter(node => !nodesWithOutgoing.has(node));
}

/**
 * Recursively extract $ref definitions from JSON schema
 * @param {*} item - JSON schema item
 * @returns {string[]} - Array of ref strings
 */
export function getAllJsonRefs(item) {
  const refs = [];

  if (Array.isArray(item)) {
    for (const element of item) {
      refs.push(...getAllJsonRefs(element));
    }
  } else if (item && typeof item === 'object') {
    for (const [key, value] of Object.entries(item)) {
      if (key === '$ref' && typeof value === 'string') {
        refs.push(value);
      } else {
        refs.push(...getAllJsonRefs(value));
      }
    }
  }

  return refs;
}

/**
 * Find all vertices involved in cycles
 * @param {Array<[string, string]>} edges - Array of [source, target] edges
 * @returns {Set<string>} - Set of nodes in cycles
 */
export function findCycleVertices(edges) {
  // Build adjacency list
  const graph = new Map();
  const allNodes = new Set();

  for (const [source, target] of edges) {
    if (!graph.has(source)) {
      graph.set(source, []);
    }
    graph.get(source).push(target);
    allNodes.add(source);
    allNodes.add(target);
  }

  const cycleVertices = new Set();
  const visited = new Set();
  const recStack = new Set();
  const path = [];

  function dfs(node) {
    visited.add(node);
    recStack.add(node);
    path.push(node);

    const neighbors = graph.get(node) || [];
    for (const neighbor of neighbors) {
      if (!visited.has(neighbor)) {
        dfs(neighbor);
      } else if (recStack.has(neighbor)) {
        // Found a cycle - add all nodes in the cycle
        const cycleStart = path.indexOf(neighbor);
        for (let i = cycleStart; i < path.length; i++) {
          cycleVertices.add(path[i]);
        }
      }
    }

    path.pop();
    recStack.delete(node);
  }

  for (const node of allNodes) {
    if (!visited.has(node)) {
      dfs(node);
    }
  }

  return cycleVertices;
}

/**
 * Sort vertices with chat inputs first
 * @param {string[][]} verticesLayers - Array of vertex layers
 * @returns {string[][]} - Sorted layers
 */
export function sortChatInputsFirst(verticesLayers) {
  return verticesLayers.map(layer => {
    const chatInputs = layer.filter(v => v.toLowerCase().includes('chat'));
    const others = layer.filter(v => !v.toLowerCase().includes('chat'));
    return [...chatInputs, ...others];
  });
}

/**
 * Find node with highest degree (most connections)
 * @param {string[]} nodes - Array of node identifiers
 * @param {Array<[string, string]>} connections - Array of [source, target] edges
 * @returns {string|null} - Node with highest degree
 */
export function findNodeWithHighestDegree(nodes, connections) {
  if (nodes.length === 0) {
    return null;
  }

  const degree = new Map();
  for (const node of nodes) {
    degree.set(node, 0);
  }

  for (const [source, target] of connections) {
    if (degree.has(source)) {
      degree.set(source, degree.get(source) + 1);
    }
    if (degree.has(target)) {
      degree.set(target, degree.get(target) + 1);
    }
  }

  let maxNode = nodes[0];
  let maxDegree = degree.get(nodes[0]);

  for (const node of nodes) {
    if (degree.get(node) > maxDegree) {
      maxDegree = degree.get(node);
      maxNode = node;
    }
  }

  return maxNode;
}

/**
 * Find connected components (clusters) using BFS
 * @param {string[]} nodes - Array of node identifiers
 * @param {Array<[string, string]>} edges - Array of [source, target] edges
 * @returns {string[][]} - Array of clusters (each cluster is array of nodes)
 */
export function findNodeClusters(nodes, edges) {
  // Build undirected adjacency list
  const graph = new Map();
  for (const node of nodes) {
    graph.set(node, []);
  }

  for (const [source, target] of edges) {
    if (graph.has(source)) {
      graph.get(source).push(target);
    }
    if (graph.has(target)) {
      graph.get(target).push(source);
    }
  }

  const visited = new Set();
  const clusters = [];

  for (const node of nodes) {
    if (!visited.has(node)) {
      const cluster = [];
      const queue = [node];
      visited.add(node);

      while (queue.length > 0) {
        const current = queue.shift();
        cluster.push(current);

        for (const neighbor of graph.get(current) || []) {
          if (!visited.has(neighbor)) {
            visited.add(neighbor);
            queue.push(neighbor);
          }
        }
      }

      clusters.push(cluster);
    }
  }

  return clusters;
}

/**
 * Calculate betweenness centrality for each node
 * @param {string[]} nodes - Array of node identifiers
 * @param {Array<[string, string]>} edges - Array of [source, target] edges
 * @returns {Map<string, number>} - Map of node to betweenness score
 */
export function calculateNodeBetweenness(nodes, edges) {
  const betweenness = new Map();
  for (const node of nodes) {
    betweenness.set(node, 0);
  }

  // Build adjacency list
  const graph = new Map();
  for (const node of nodes) {
    graph.set(node, []);
  }
  for (const [source, target] of edges) {
    if (graph.has(source)) {
      graph.get(source).push(target);
    }
  }

  // For each pair of nodes, find shortest paths and count intermediaries
  for (const source of nodes) {
    // BFS from source
    const dist = new Map();
    const paths = new Map();
    const pred = new Map();

    for (const node of nodes) {
      dist.set(node, Infinity);
      paths.set(node, 0);
      pred.set(node, []);
    }

    dist.set(source, 0);
    paths.set(source, 1);

    const queue = [source];
    const stack = [];

    while (queue.length > 0) {
      const current = queue.shift();
      stack.push(current);

      for (const neighbor of graph.get(current) || []) {
        if (dist.get(neighbor) === Infinity) {
          dist.set(neighbor, dist.get(current) + 1);
          queue.push(neighbor);
        }

        if (dist.get(neighbor) === dist.get(current) + 1) {
          paths.set(neighbor, paths.get(neighbor) + paths.get(current));
          pred.get(neighbor).push(current);
        }
      }
    }

    // Accumulate betweenness
    const delta = new Map();
    for (const node of nodes) {
      delta.set(node, 0);
    }

    while (stack.length > 0) {
      const w = stack.pop();
      for (const v of pred.get(w)) {
        const contribution = (paths.get(v) / paths.get(w)) * (1 + delta.get(w));
        delta.set(v, delta.get(v) + contribution);
      }
      if (w !== source) {
        betweenness.set(w, betweenness.get(w) + delta.get(w));
      }
    }
  }

  return betweenness;
}

/**
 * Find strongly connected components using Kosaraju's algorithm
 * @param {string[]} nodes - Array of node identifiers
 * @param {Array<[string, string]>} edges - Array of [source, target] edges
 * @returns {string[][]} - Array of SCCs
 */
export function findStronglyConnectedComponents(nodes, edges) {
  // Build adjacency list and reverse graph
  const graph = new Map();
  const reverseGraph = new Map();

  for (const node of nodes) {
    graph.set(node, []);
    reverseGraph.set(node, []);
  }

  for (const [source, target] of edges) {
    if (graph.has(source)) {
      graph.get(source).push(target);
    }
    if (reverseGraph.has(target)) {
      reverseGraph.get(target).push(source);
    }
  }

  // First DFS to get finish order
  const visited = new Set();
  const finishOrder = [];

  function dfs1(node) {
    visited.add(node);
    for (const neighbor of graph.get(node) || []) {
      if (!visited.has(neighbor)) {
        dfs1(neighbor);
      }
    }
    finishOrder.push(node);
  }

  for (const node of nodes) {
    if (!visited.has(node)) {
      dfs1(node);
    }
  }

  // Second DFS on reverse graph in reverse finish order
  visited.clear();
  const sccs = [];

  function dfs2(node, component) {
    visited.add(node);
    component.push(node);
    for (const neighbor of reverseGraph.get(node) || []) {
      if (!visited.has(neighbor)) {
        dfs2(neighbor, component);
      }
    }
  }

  while (finishOrder.length > 0) {
    const node = finishOrder.pop();
    if (!visited.has(node)) {
      const component = [];
      dfs2(node, component);
      sccs.push(component);
    }
  }

  return sccs;
}
