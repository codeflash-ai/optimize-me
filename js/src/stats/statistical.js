/**
 * Statistical and Machine Learning Functions
 * JavaScript equivalents of Python/NumPy/Pandas implementations
 */

/**
 * Compute mean of array
 * @param {number[]} arr - Input array
 * @returns {number} - Mean value
 */
export function mean(arr) {
  if (arr.length === 0) return NaN;
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}

/**
 * Compute standard deviation
 * @param {number[]} arr - Input array
 * @param {boolean} sample - Whether to use sample std (n-1)
 * @returns {number} - Standard deviation
 */
export function std(arr, sample = false) {
  if (arr.length === 0) return NaN;
  const m = mean(arr);
  const squaredDiffs = arr.map(x => (x - m) ** 2);
  const divisor = sample ? arr.length - 1 : arr.length;
  return Math.sqrt(squaredDiffs.reduce((a, b) => a + b, 0) / divisor);
}

/**
 * Compute variance
 * @param {number[]} arr - Input array
 * @param {boolean} sample - Whether to use sample variance (n-1)
 * @returns {number} - Variance
 */
export function variance(arr, sample = false) {
  const s = std(arr, sample);
  return s * s;
}

/**
 * Compute median
 * @param {number[]} arr - Input array
 * @returns {number} - Median value
 */
export function median(arr) {
  if (arr.length === 0) return NaN;
  const sorted = [...arr].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  if (sorted.length % 2 === 0) {
    return (sorted[mid - 1] + sorted[mid]) / 2;
  }
  return sorted[mid];
}

/**
 * Compute descriptive statistics
 * @param {number[]} series - Input series
 * @returns {Object} - Statistics object
 */
export function describe(series) {
  const sorted = [...series].sort((a, b) => a - b);
  const n = series.length;

  return {
    count: n,
    mean: mean(series),
    std: std(series),
    min: sorted[0],
    '25%': sorted[Math.floor(n * 0.25)],
    '50%': median(series),
    '75%': sorted[Math.floor(n * 0.75)],
    max: sorted[n - 1]
  };
}

/**
 * Cosine similarity between two vectors
 * @param {number[]} a - First vector
 * @param {number[]} b - Second vector
 * @returns {number} - Cosine similarity (-1 to 1)
 */
export function cosineSimilarityVectors(a, b) {
  let dotProduct = 0;
  let normA = 0;
  let normB = 0;

  for (let i = 0; i < a.length; i++) {
    dotProduct += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }

  const denominator = Math.sqrt(normA) * Math.sqrt(normB);
  if (denominator === 0) return 0;

  return dotProduct / denominator;
}

/**
 * Cosine similarity matrix between two sets of vectors
 * @param {number[][]} X - First matrix (rows are vectors)
 * @param {number[][]} Y - Second matrix (rows are vectors)
 * @returns {number[][]} - Similarity matrix
 */
export function cosineSimilarity(X, Y) {
  const result = [];

  for (let i = 0; i < X.length; i++) {
    const row = [];
    for (let j = 0; j < Y.length; j++) {
      row.push(cosineSimilarityVectors(X[i], Y[j]));
    }
    result.push(row);
  }

  return result;
}

/**
 * Cosine similarity with top-k filtering
 * @param {number[][]} X - First matrix
 * @param {number[][]} Y - Second matrix
 * @param {number} topK - Number of top matches to return
 * @param {number} scoreThreshold - Minimum score threshold
 * @returns {Array<{xIndex: number, yIndex: number, score: number}>[]} - Top matches for each X row
 */
export function cosineSimilarityTopK(X, Y, topK = 5, scoreThreshold = 0) {
  const results = [];

  for (let i = 0; i < X.length; i++) {
    const scores = [];
    for (let j = 0; j < Y.length; j++) {
      const score = cosineSimilarityVectors(X[i], Y[j]);
      if (score >= scoreThreshold) {
        scores.push({ xIndex: i, yIndex: j, score });
      }
    }

    // Sort by score descending and take top k
    scores.sort((a, b) => b.score - a.score);
    results.push(scores.slice(0, topK));
  }

  return results;
}

/**
 * Pearson correlation coefficient
 * @param {number[]} x - First array
 * @param {number[]} y - Second array
 * @returns {number} - Correlation coefficient
 */
export function pearsonCorrelation(x, y) {
  const n = x.length;
  const meanX = mean(x);
  const meanY = mean(y);

  let numerator = 0;
  let denomX = 0;
  let denomY = 0;

  for (let i = 0; i < n; i++) {
    const dx = x[i] - meanX;
    const dy = y[i] - meanY;
    numerator += dx * dy;
    denomX += dx * dx;
    denomY += dy * dy;
  }

  const denominator = Math.sqrt(denomX) * Math.sqrt(denomY);
  if (denominator === 0) return 0;

  return numerator / denominator;
}

/**
 * Correlation matrix for dataframe-like object
 * @param {Object} df - Object with column arrays
 * @returns {Object} - Correlation matrix as object
 */
export function correlation(df) {
  const columns = Object.keys(df);
  const result = {};

  for (const col1 of columns) {
    result[col1] = {};
    for (const col2 of columns) {
      result[col1][col2] = pearsonCorrelation(df[col1], df[col2]);
    }
  }

  return result;
}

/**
 * Principal Component Analysis
 * @param {number[][]} X - Data matrix (rows are samples)
 * @param {number} nComponents - Number of components
 * @returns {{components: number[][], explained: number[], transformed: number[][]}} - PCA result
 */
export function pca(X, nComponents) {
  const n = X.length;
  const m = X[0].length;

  // Center the data
  const means = Array(m).fill(0);
  for (let j = 0; j < m; j++) {
    for (let i = 0; i < n; i++) {
      means[j] += X[i][j];
    }
    means[j] /= n;
  }

  const centered = X.map(row =>
    row.map((val, j) => val - means[j])
  );

  // Compute covariance matrix
  const cov = Array(m).fill(null).map(() => Array(m).fill(0));
  for (let i = 0; i < m; i++) {
    for (let j = 0; j < m; j++) {
      let sum = 0;
      for (let k = 0; k < n; k++) {
        sum += centered[k][i] * centered[k][j];
      }
      cov[i][j] = sum / (n - 1);
    }
  }

  // Power iteration to find principal components (simplified)
  const components = [];
  const eigenvalues = [];
  const covCopy = cov.map(row => [...row]);

  for (let c = 0; c < nComponents; c++) {
    // Initialize random vector
    let v = Array(m).fill(0).map(() => Math.random() - 0.5);
    let norm = Math.sqrt(v.reduce((a, b) => a + b * b, 0));
    v = v.map(x => x / norm);

    // Power iteration
    for (let iter = 0; iter < 100; iter++) {
      // Multiply by covariance matrix
      const newV = Array(m).fill(0);
      for (let i = 0; i < m; i++) {
        for (let j = 0; j < m; j++) {
          newV[i] += covCopy[i][j] * v[j];
        }
      }

      // Normalize
      norm = Math.sqrt(newV.reduce((a, b) => a + b * b, 0));
      if (norm > 0) {
        v = newV.map(x => x / norm);
      }
    }

    // Compute eigenvalue
    let eigenvalue = 0;
    const Av = Array(m).fill(0);
    for (let i = 0; i < m; i++) {
      for (let j = 0; j < m; j++) {
        Av[i] += covCopy[i][j] * v[j];
      }
    }
    for (let i = 0; i < m; i++) {
      eigenvalue += v[i] * Av[i];
    }

    components.push(v);
    eigenvalues.push(eigenvalue);

    // Deflate covariance matrix
    for (let i = 0; i < m; i++) {
      for (let j = 0; j < m; j++) {
        covCopy[i][j] -= eigenvalue * v[i] * v[j];
      }
    }
  }

  // Transform data
  const transformed = centered.map(row => {
    return components.map(comp => {
      let dot = 0;
      for (let i = 0; i < m; i++) {
        dot += row[i] * comp[i];
      }
      return dot;
    });
  });

  // Compute explained variance ratio
  const totalVariance = eigenvalues.reduce((a, b) => a + Math.abs(b), 0);
  const explained = eigenvalues.map(e => Math.abs(e) / totalVariance);

  return { components, explained, transformed };
}

/**
 * K-Means clustering
 * @param {number[][]} X - Data matrix
 * @param {number} k - Number of clusters
 * @param {number} maxIter - Maximum iterations
 * @returns {{centroids: number[][], labels: number[]}} - Cluster result
 */
export function kmeansClustering(X, k, maxIter = 100) {
  const n = X.length;
  const m = X[0].length;

  // Initialize centroids randomly
  const indices = [];
  while (indices.length < k) {
    const idx = Math.floor(Math.random() * n);
    if (!indices.includes(idx)) {
      indices.push(idx);
    }
  }
  let centroids = indices.map(i => [...X[i]]);

  let labels = Array(n).fill(0);

  for (let iter = 0; iter < maxIter; iter++) {
    // Assign points to nearest centroid
    const newLabels = X.map(point => {
      let minDist = Infinity;
      let label = 0;
      for (let c = 0; c < k; c++) {
        let dist = 0;
        for (let j = 0; j < m; j++) {
          dist += (point[j] - centroids[c][j]) ** 2;
        }
        if (dist < minDist) {
          minDist = dist;
          label = c;
        }
      }
      return label;
    });

    // Check convergence
    let changed = false;
    for (let i = 0; i < n; i++) {
      if (newLabels[i] !== labels[i]) {
        changed = true;
        break;
      }
    }
    labels = newLabels;

    if (!changed) break;

    // Update centroids
    const newCentroids = Array(k).fill(null).map(() => Array(m).fill(0));
    const counts = Array(k).fill(0);

    for (let i = 0; i < n; i++) {
      const c = labels[i];
      counts[c]++;
      for (let j = 0; j < m; j++) {
        newCentroids[c][j] += X[i][j];
      }
    }

    for (let c = 0; c < k; c++) {
      if (counts[c] > 0) {
        for (let j = 0; j < m; j++) {
          newCentroids[c][j] /= counts[c];
        }
      }
    }

    centroids = newCentroids;
  }

  return { centroids, labels };
}

/**
 * Gradient descent for linear regression
 * @param {number[][]} X - Feature matrix
 * @param {number[]} y - Target values
 * @param {number} learningRate - Learning rate
 * @param {number} iterations - Number of iterations
 * @returns {{weights: number[], bias: number}} - Trained parameters
 */
export function gradientDescent(X, y, learningRate = 0.01, iterations = 1000) {
  const n = X.length;
  const m = X[0].length;

  // Initialize weights and bias
  let weights = Array(m).fill(0);
  let bias = 0;

  for (let iter = 0; iter < iterations; iter++) {
    // Compute predictions
    const predictions = X.map(row => {
      let pred = bias;
      for (let j = 0; j < m; j++) {
        pred += row[j] * weights[j];
      }
      return pred;
    });

    // Compute gradients
    const errors = predictions.map((p, i) => p - y[i]);

    const gradWeights = Array(m).fill(0);
    for (let j = 0; j < m; j++) {
      for (let i = 0; i < n; i++) {
        gradWeights[j] += errors[i] * X[i][j];
      }
      gradWeights[j] /= n;
    }

    let gradBias = 0;
    for (let i = 0; i < n; i++) {
      gradBias += errors[i];
    }
    gradBias /= n;

    // Update parameters
    for (let j = 0; j < m; j++) {
      weights[j] -= learningRate * gradWeights[j];
    }
    bias -= learningRate * gradBias;
  }

  return { weights, bias };
}

/**
 * Predict using linear regression model
 * @param {number[][]} X - Feature matrix
 * @param {number[]} weights - Model weights
 * @param {number} bias - Model bias
 * @returns {number[]} - Predictions
 */
export function linearPredict(X, weights, bias) {
  return X.map(row => {
    let pred = bias;
    for (let j = 0; j < row.length; j++) {
      pred += row[j] * weights[j];
    }
    return pred;
  });
}
