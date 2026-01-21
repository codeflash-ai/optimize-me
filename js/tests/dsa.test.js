/**
 * Tests for DSA Module
 */

import {
  timeBasedCache,
  matrixChainOrder,
  binomialCoefficient,
  coinChange,
  knapsack
} from '../src/dsa/cachingMemoization.js';

import {
  findLastNode,
  findLeafNodes,
  getAllJsonRefs,
  findCycleVertices,
  sortChatInputsFirst,
  findNodeWithHighestDegree,
  findNodeClusters,
  calculateNodeBetweenness,
  findStronglyConnectedComponents
} from '../src/dsa/nodes.js';

import {
  Graph,
  Stack,
  fibonacci,
  stringConcat,
  matrixSum,
  graphTraversal,
  regexMatch,
  isPalindrome,
  wordFrequency,
  PathFinder
} from '../src/dsa/various.js';

// Caching and Memoization Tests
describe('Caching and Memoization', () => {
  describe('matrixChainOrder', () => {
    test('empty matrices', () => {
      expect(matrixChainOrder([])).toBe(0);
    });

    test('single matrix', () => {
      expect(matrixChainOrder([[10, 20]])).toBe(0);
    });

    test('two matrices', () => {
      expect(matrixChainOrder([[10, 20], [20, 30]])).toBe(6000);
    });

    test('three matrices', () => {
      expect(matrixChainOrder([[10, 20], [20, 30], [30, 40]])).toBe(18000);
    });

    test('four matrices optimal ordering', () => {
      expect(matrixChainOrder([[40, 20], [20, 30], [30, 10], [10, 30]])).toBe(26000);
    });
  });

  describe('binomialCoefficient', () => {
    test('C(0,0) = 1', () => {
      expect(binomialCoefficient(0, 0)).toBe(1);
    });

    test('C(5,0) = 1', () => {
      expect(binomialCoefficient(5, 0)).toBe(1);
    });

    test('C(5,5) = 1', () => {
      expect(binomialCoefficient(5, 5)).toBe(1);
    });

    test('C(5,2) = 10', () => {
      expect(binomialCoefficient(5, 2)).toBe(10);
    });

    test('C(10,3) = 120', () => {
      expect(binomialCoefficient(10, 3)).toBe(120);
    });

    test('C(3,5) = 0 (k > n)', () => {
      expect(binomialCoefficient(3, 5)).toBe(0);
    });
  });

  describe('coinChange', () => {
    test('zero amount', () => {
      expect(coinChange([1, 2, 5], 0)).toBe(1);
    });

    test('simple case', () => {
      expect(coinChange([1, 2], 4)).toBe(3);
    });

    test('single coin', () => {
      expect(coinChange([2], 4)).toBe(1);
    });

    test('impossible amount', () => {
      expect(coinChange([2], 3)).toBe(0);
    });
  });

  describe('knapsack', () => {
    test('empty knapsack', () => {
      expect(knapsack([], [], 10)).toBe(0);
    });

    test('zero capacity', () => {
      expect(knapsack([1, 2], [10, 20], 0)).toBe(0);
    });

    test('simple case', () => {
      expect(knapsack([10, 20, 30], [60, 100, 120], 50)).toBe(220);
    });

    test('all items fit', () => {
      expect(knapsack([1, 2, 3], [10, 20, 30], 10)).toBe(60);
    });
  });
});

// Node Operations Tests
describe('Node Operations', () => {
  describe('findLastNode', () => {
    test('simple linear graph', () => {
      expect(findLastNode(['A', 'B', 'C'], [['A', 'B'], ['B', 'C']])).toBe('C');
    });

    test('single node', () => {
      expect(findLastNode(['A'], [])).toBe('A');
    });

    test('multiple leaves returns first found', () => {
      const result = findLastNode(['A', 'B', 'C'], [['A', 'B'], ['A', 'C']]);
      expect(['B', 'C']).toContain(result);
    });
  });

  describe('findLeafNodes', () => {
    test('simple graph', () => {
      const leaves = findLeafNodes(['A', 'B', 'C'], [['A', 'B'], ['A', 'C']]);
      expect(leaves.sort()).toEqual(['B', 'C']);
    });

    test('no edges', () => {
      expect(findLeafNodes(['A', 'B'], [])).toEqual(['A', 'B']);
    });

    test('linear graph', () => {
      expect(findLeafNodes(['A', 'B', 'C'], [['A', 'B'], ['B', 'C']])).toEqual(['C']);
    });
  });

  describe('getAllJsonRefs', () => {
    test('simple ref', () => {
      expect(getAllJsonRefs({ '$ref': '#/defs/User' })).toEqual(['#/defs/User']);
    });

    test('nested refs', () => {
      const schema = {
        type: 'object',
        properties: {
          user: { '$ref': '#/defs/User' },
          address: { '$ref': '#/defs/Address' }
        }
      };
      expect(getAllJsonRefs(schema).sort()).toEqual(['#/defs/Address', '#/defs/User']);
    });

    test('array with refs', () => {
      expect(getAllJsonRefs([{ '$ref': 'A' }, { '$ref': 'B' }]).sort()).toEqual(['A', 'B']);
    });

    test('no refs', () => {
      expect(getAllJsonRefs({ type: 'string' })).toEqual([]);
    });
  });

  describe('findCycleVertices', () => {
    test('simple cycle', () => {
      const edges = [['A', 'B'], ['B', 'C'], ['C', 'A']];
      const result = findCycleVertices(edges);
      expect(result.size).toBe(3);
      expect(result.has('A')).toBe(true);
      expect(result.has('B')).toBe(true);
      expect(result.has('C')).toBe(true);
    });

    test('no cycle', () => {
      const edges = [['A', 'B'], ['B', 'C']];
      expect(findCycleVertices(edges).size).toBe(0);
    });

    test('self loop', () => {
      const edges = [['A', 'A']];
      expect(findCycleVertices(edges).has('A')).toBe(true);
    });

    test('empty graph', () => {
      expect(findCycleVertices([]).size).toBe(0);
    });
  });

  describe('findNodeClusters', () => {
    test('two clusters', () => {
      const nodes = ['A', 'B', 'C', 'D'];
      const edges = [['A', 'B'], ['C', 'D']];
      const clusters = findNodeClusters(nodes, edges);
      expect(clusters.length).toBe(2);
    });

    test('single cluster', () => {
      const nodes = ['A', 'B', 'C'];
      const edges = [['A', 'B'], ['B', 'C']];
      const clusters = findNodeClusters(nodes, edges);
      expect(clusters.length).toBe(1);
    });

    test('isolated nodes', () => {
      const nodes = ['A', 'B', 'C'];
      const edges = [];
      const clusters = findNodeClusters(nodes, edges);
      expect(clusters.length).toBe(3);
    });
  });

  describe('findStronglyConnectedComponents', () => {
    test('simple SCC', () => {
      const nodes = ['A', 'B', 'C'];
      const edges = [['A', 'B'], ['B', 'C'], ['C', 'A']];
      const sccs = findStronglyConnectedComponents(nodes, edges);
      expect(sccs.length).toBe(1);
      expect(sccs[0].sort()).toEqual(['A', 'B', 'C']);
    });

    test('multiple SCCs', () => {
      const nodes = ['A', 'B', 'C', 'D'];
      const edges = [['A', 'B'], ['B', 'A'], ['C', 'D']];
      const sccs = findStronglyConnectedComponents(nodes, edges);
      expect(sccs.length).toBe(3);
    });
  });
});

// Various Data Structures Tests
describe('Various Data Structures', () => {
  describe('Graph', () => {
    test('add and get edges', () => {
      const g = new Graph();
      g.addEdge('A', 'B');
      g.addEdge('B', 'C');
      expect(g.getEdges()).toEqual([['A', 'B'], ['B', 'C']]);
    });

    test('hasEdge', () => {
      const g = new Graph();
      g.addEdge('A', 'B');
      expect(g.hasEdge('A', 'B')).toBe(true);
      expect(g.hasEdge('B', 'A')).toBe(false);
    });
  });

  describe('Stack', () => {
    test('push and size', () => {
      const s = new Stack();
      s.push(1);
      s.push(2);
      expect(s.size()).toBe(2);
    });

    test('peek', () => {
      const s = new Stack();
      s.push(1);
      s.push(2);
      expect(s.peek()).toBe(2);
    });

    test('isEmpty', () => {
      const s = new Stack();
      expect(s.isEmpty()).toBe(true);
      s.push(1);
      expect(s.isEmpty()).toBe(false);
    });
  });

  describe('fibonacci', () => {
    test('fib(0) = 0', () => {
      expect(fibonacci(0)).toBe(0);
    });

    test('fib(1) = 1', () => {
      expect(fibonacci(1)).toBe(1);
    });

    test('fib(10) = 55', () => {
      expect(fibonacci(10)).toBe(55);
    });

    test('fib(15) = 610', () => {
      expect(fibonacci(15)).toBe(610);
    });
  });

  describe('stringConcat', () => {
    test('empty string', () => {
      expect(stringConcat(0)).toBe('');
    });

    test('small n', () => {
      expect(stringConcat(5)).toBe('01234');
    });
  });

  describe('matrixSum', () => {
    test('positive sums', () => {
      expect(matrixSum([[1, 2], [3, 4]])).toEqual([3, 7]);
    });

    test('filter negative sums', () => {
      expect(matrixSum([[1, -5], [3, 4]])).toEqual([7]);
    });

    test('empty matrix', () => {
      expect(matrixSum([])).toEqual([]);
    });
  });

  describe('isPalindrome', () => {
    test('simple palindrome', () => {
      expect(isPalindrome('racecar')).toBe(true);
    });

    test('with spaces and punctuation', () => {
      expect(isPalindrome('A man, a plan, a canal: Panama')).toBe(true);
    });

    test('not palindrome', () => {
      expect(isPalindrome('hello')).toBe(false);
    });

    test('empty string', () => {
      expect(isPalindrome('')).toBe(true);
    });
  });

  describe('wordFrequency', () => {
    test('simple text', () => {
      const freq = wordFrequency('hello world hello');
      expect(freq.get('hello')).toBe(2);
      expect(freq.get('world')).toBe(1);
    });

    test('empty text', () => {
      const freq = wordFrequency('');
      expect(freq.size).toBe(0);
    });
  });

  describe('regexMatch', () => {
    test('simple pattern', () => {
      expect(regexMatch(['abc', 'def', 'abcd'], 'abc')).toEqual(['abc', 'abcd']);
    });

    test('no matches', () => {
      expect(regexMatch(['abc', 'def'], 'xyz')).toEqual([]);
    });
  });

  describe('PathFinder', () => {
    test('find shortest path', () => {
      const graph = new Map([
        ['A', ['B', 'C']],
        ['B', ['D']],
        ['C', ['D']],
        ['D', []]
      ]);
      const pf = new PathFinder(graph);
      expect(pf.findShortestPath('A', 'D')).toEqual(['A', 'B', 'D']);
    });

    test('no path exists', () => {
      const graph = new Map([
        ['A', ['B']],
        ['B', []],
        ['C', ['D']],
        ['D', []]
      ]);
      const pf = new PathFinder(graph);
      expect(pf.findShortestPath('A', 'D')).toBeNull();
    });

    test('same start and end', () => {
      const graph = new Map([['A', ['B']]]);
      const pf = new PathFinder(graph);
      expect(pf.findShortestPath('A', 'A')).toEqual(['A']);
    });
  });
});
