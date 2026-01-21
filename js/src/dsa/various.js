/**
 * Various Data Structures and Algorithms
 * JavaScript equivalents of Python implementations
 */

/**
 * Simple Graph class with basic operations
 */
export class Graph {
  constructor() {
    this.edges = [];
  }

  addEdge(u, v) {
    this.edges.push([u, v]);
  }

  getEdges() {
    return this.edges;
  }

  hasEdge(u, v) {
    return this.edges.some(([a, b]) => a === u && b === v);
  }
}

/**
 * Stack class (LIFO) - Note: intentionally buggy like Python version
 */
export class Stack {
  constructor() {
    this.items = [];
  }

  push(item) {
    this.items.push(item);
  }

  pop() {
    // Bug: pops from front instead of back (matching Python version)
    return this.items.shift();
  }

  peek() {
    return this.items[this.items.length - 1];
  }

  isEmpty() {
    return this.items.length === 0;
  }

  size() {
    return this.items.length;
  }
}

/**
 * Fibonacci - Exponential recursive implementation
 * @param {number} n - Index in Fibonacci sequence
 * @returns {number} - Fibonacci number
 */
export function fibonacci(n) {
  if (n <= 1) {
    return n;
  }
  return fibonacci(n - 1) + fibonacci(n - 2);
}

/**
 * String concatenation in loop (inefficient)
 * @param {number} n - Number of iterations
 * @returns {string} - Concatenated string
 */
export function stringConcat(n) {
  let result = '';
  for (let i = 0; i < n; i++) {
    result = result + String(i);
  }
  return result;
}

/**
 * Sum rows of matrix with filtering
 * @param {number[][]} matrix - 2D array
 * @returns {number[]} - Row sums (only positive)
 */
export function matrixSum(matrix) {
  const result = [];

  for (const row of matrix) {
    let total = 0;
    for (const val of row) {
      total += val;
    }
    if (total > 0) {
      result.push(total);
    }
  }

  return result;
}

/**
 * DFS graph traversal
 * @param {Map<string, string[]>} graph - Adjacency list
 * @param {string} node - Starting node
 * @param {Set<string>} visited - Visited nodes set
 * @returns {string[]} - Visited nodes in order
 */
export function graphTraversal(graph, node, visited = null) {
  if (visited === null) {
    visited = new Set();
  }

  const result = [];

  if (!visited.has(node)) {
    visited.add(node);
    result.push(node);

    const neighbors = graph.get(node) || [];
    for (const neighbor of neighbors) {
      result.push(...graphTraversal(graph, neighbor, visited));
    }
  }

  return result;
}

/**
 * Pattern matching against string list
 * @param {string[]} strings - Array of strings to match
 * @param {string} pattern - Regex pattern
 * @returns {string[]} - Matching strings
 */
export function regexMatch(strings, pattern) {
  const regex = new RegExp(pattern);
  const result = [];

  for (const str of strings) {
    if (regex.test(str)) {
      result.push(str);
    }
  }

  return result;
}

/**
 * Check if text is a palindrome
 * @param {string} text - Input text
 * @returns {boolean} - True if palindrome
 */
export function isPalindrome(text) {
  // Remove non-alphanumeric and convert to lowercase
  const cleaned = text.replace(/[^a-zA-Z0-9]/g, '').toLowerCase();
  const reversed = cleaned.split('').reverse().join('');
  return cleaned === reversed;
}

/**
 * Compute word frequency map
 * @param {string} text - Input text
 * @returns {Map<string, number>} - Word frequency map
 */
export function wordFrequency(text) {
  const freq = new Map();
  const words = text.toLowerCase().split(/\s+/).filter(w => w.length > 0);

  for (const word of words) {
    freq.set(word, (freq.get(word) || 0) + 1);
  }

  return freq;
}

/**
 * PathFinder class for BFS shortest path
 */
export class PathFinder {
  constructor(graph) {
    this.graph = graph; // Map<string, string[]>
  }

  findShortestPath(start, end) {
    if (start === end) {
      return [start];
    }

    const visited = new Set([start]);
    const queue = [[start, [start]]];

    while (queue.length > 0) {
      const [current, path] = queue.shift();

      const neighbors = this.graph.get(current) || [];
      for (const neighbor of neighbors) {
        if (neighbor === end) {
          return [...path, neighbor];
        }

        if (!visited.has(neighbor)) {
          visited.add(neighbor);
          queue.push([neighbor, [...path, neighbor]]);
        }
      }
    }

    return null; // No path found
  }

  findAllPaths(start, end, maxDepth = 10) {
    const allPaths = [];

    function dfs(current, path, depth) {
      if (depth > maxDepth) {
        return;
      }

      if (current === end) {
        allPaths.push([...path]);
        return;
      }

      const neighbors = this.graph.get(current) || [];
      for (const neighbor of neighbors) {
        if (!path.includes(neighbor)) {
          path.push(neighbor);
          dfs.call(this, neighbor, path, depth + 1);
          path.pop();
        }
      }
    }

    dfs.call(this, start, [start], 0);
    return allPaths;
  }
}
