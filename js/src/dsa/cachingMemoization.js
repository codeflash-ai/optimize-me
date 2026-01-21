/**
 * Caching and Memoization Algorithms
 * JavaScript equivalents of Python implementations
 */

/**
 * Creates a time-based cache decorator
 * @param {number} expirySeconds - Cache expiry time in seconds
 * @returns {Function} - Decorator function
 */
export function timeBasedCache(expirySeconds) {
  const cache = new Map();

  return function(fn) {
    return function(...args) {
      const key = args.map(arg => {
        if (typeof arg === 'object') {
          return JSON.stringify(arg);
        }
        return String(arg);
      }).join('_');

      const now = Date.now() / 1000;

      if (cache.has(key)) {
        const [value, timestamp] = cache.get(key);
        if (now - timestamp < expirySeconds) {
          return value;
        }
      }

      const result = fn(...args);
      cache.set(key, [result, now]);
      return result;
    };
  };
}

/**
 * Matrix Chain Order - Dynamic Programming
 * Finds minimum number of scalar multiplications needed for matrix chain multiplication
 * @param {Array<[number, number]>} matrices - Array of [rows, cols] for each matrix
 * @returns {number} - Minimum number of multiplications
 */
export function matrixChainOrder(matrices) {
  if (!matrices || matrices.length === 0) {
    return 0;
  }

  const n = matrices.length;
  if (n === 1) {
    return 0;
  }

  // Create dimensions array: p[i] is rows of matrix i, p[i+1] is cols of matrix i
  const p = [matrices[0][0]];
  for (const [, cols] of matrices) {
    p.push(cols);
  }

  // m[i][j] = minimum multiplications for matrices i to j
  const m = Array(n).fill(null).map(() => Array(n).fill(0));

  // l is chain length
  for (let l = 2; l <= n; l++) {
    for (let i = 0; i <= n - l; i++) {
      const j = i + l - 1;
      m[i][j] = Infinity;

      for (let k = i; k < j; k++) {
        const cost = m[i][k] + m[k + 1][j] + p[i] * p[k + 1] * p[j + 1];
        if (cost < m[i][j]) {
          m[i][j] = cost;
        }
      }
    }
  }

  return m[0][n - 1];
}

/**
 * Binomial Coefficient - Recursive implementation
 * @param {number} n - Total items
 * @param {number} k - Items to choose
 * @returns {number} - C(n, k)
 */
export function binomialCoefficient(n, k) {
  if (k === 0 || k === n) {
    return 1;
  }
  if (k > n || k < 0 || n < 0) {
    return 0;
  }
  return binomialCoefficient(n - 1, k - 1) + binomialCoefficient(n - 1, k);
}

/**
 * Coin Change Problem - Recursive implementation
 * @param {number[]} coins - Available coin denominations
 * @param {number} amount - Target amount
 * @param {number} index - Current coin index
 * @returns {number} - Number of ways to make change
 */
export function coinChange(coins, amount, index = 0) {
  if (amount === 0) {
    return 1;
  }
  if (amount < 0 || index >= coins.length) {
    return 0;
  }

  // Include current coin or skip to next
  return coinChange(coins, amount - coins[index], index) +
         coinChange(coins, amount, index + 1);
}

/**
 * 0/1 Knapsack Problem - Recursive implementation
 * @param {number[]} weights - Item weights
 * @param {number[]} values - Item values
 * @param {number} capacity - Knapsack capacity
 * @param {number} n - Number of items to consider
 * @returns {number} - Maximum value achievable
 */
export function knapsack(weights, values, capacity, n = null) {
  if (n === null) {
    n = weights.length;
  }

  if (n === 0 || capacity === 0) {
    return 0;
  }

  // If weight of nth item is more than capacity, skip it
  if (weights[n - 1] > capacity) {
    return knapsack(weights, values, capacity, n - 1);
  }

  // Return max of including or excluding the item
  const include = values[n - 1] + knapsack(weights, values, capacity - weights[n - 1], n - 1);
  const exclude = knapsack(weights, values, capacity, n - 1);

  return Math.max(include, exclude);
}
