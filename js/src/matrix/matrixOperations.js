/**
 * Matrix Operations
 * JavaScript equivalents of Python/NumPy implementations
 */

/**
 * Matrix multiplication
 * @param {number[][]} A - First matrix
 * @param {number[][]} B - Second matrix
 * @returns {number[][]} - Product matrix A * B
 */
export function matrixMultiply(A, B) {
  const rowsA = A.length;
  const colsA = A[0].length;
  const colsB = B[0].length;

  // Initialize result matrix with zeros
  const result = Array(rowsA).fill(null).map(() => Array(colsB).fill(0));

  for (let i = 0; i < rowsA; i++) {
    for (let j = 0; j < colsB; j++) {
      for (let k = 0; k < colsA; k++) {
        result[i][j] += A[i][k] * B[k][j];
      }
    }
  }

  return result;
}

/**
 * Vector dot product
 * @param {number[]} a - First vector
 * @param {number[]} b - Second vector
 * @returns {number} - Dot product
 */
export function dotProduct(a, b) {
  if (a.length !== b.length) {
    throw new Error('Vectors must have the same length');
  }

  let result = 0;
  for (let i = 0; i < a.length; i++) {
    result += a[i] * b[i];
  }

  return result;
}

/**
 * Matrix inverse using Gauss-Jordan elimination
 * @param {number[][]} matrix - Square matrix to invert
 * @returns {number[][]} - Inverse matrix
 */
export function matrixInverse(matrix) {
  const n = matrix.length;

  // Create augmented matrix [A | I]
  const augmented = matrix.map((row, i) => {
    const identityRow = Array(n).fill(0);
    identityRow[i] = 1;
    return [...row, ...identityRow];
  });

  // Gauss-Jordan elimination
  for (let col = 0; col < n; col++) {
    // Find pivot
    let maxRow = col;
    for (let row = col + 1; row < n; row++) {
      if (Math.abs(augmented[row][col]) > Math.abs(augmented[maxRow][col])) {
        maxRow = row;
      }
    }

    // Swap rows
    [augmented[col], augmented[maxRow]] = [augmented[maxRow], augmented[col]];

    // Check for singular matrix
    if (Math.abs(augmented[col][col]) < 1e-10) {
      throw new Error('Matrix is singular and cannot be inverted');
    }

    // Scale pivot row
    const pivot = augmented[col][col];
    for (let j = 0; j < 2 * n; j++) {
      augmented[col][j] /= pivot;
    }

    // Eliminate column
    for (let row = 0; row < n; row++) {
      if (row !== col) {
        const factor = augmented[row][col];
        for (let j = 0; j < 2 * n; j++) {
          augmented[row][j] -= factor * augmented[col][j];
        }
      }
    }
  }

  // Extract inverse (right half of augmented matrix)
  return augmented.map(row => row.slice(n));
}

/**
 * Matrix determinant using cofactor expansion
 * @param {number[][]} matrix - Square matrix
 * @returns {number} - Determinant
 */
export function matrixDeterminant(matrix) {
  const n = matrix.length;

  if (n === 1) {
    return matrix[0][0];
  }

  if (n === 2) {
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];
  }

  let det = 0;

  for (let col = 0; col < n; col++) {
    // Create minor matrix
    const minor = matrix.slice(1).map(row =>
      row.filter((_, j) => j !== col)
    );

    const sign = col % 2 === 0 ? 1 : -1;
    det += sign * matrix[0][col] * matrixDeterminant(minor);
  }

  return det;
}

/**
 * LU Decomposition
 * @param {number[][]} A - Square matrix
 * @returns {{L: number[][], U: number[][]}} - L and U matrices
 */
export function luDecomposition(A) {
  const n = A.length;

  // Initialize L and U
  const L = Array(n).fill(null).map(() => Array(n).fill(0));
  const U = Array(n).fill(null).map(() => Array(n).fill(0));

  for (let i = 0; i < n; i++) {
    L[i][i] = 1;
  }

  for (let j = 0; j < n; j++) {
    // Upper triangular
    for (let i = 0; i <= j; i++) {
      let sum = 0;
      for (let k = 0; k < i; k++) {
        sum += L[i][k] * U[k][j];
      }
      U[i][j] = A[i][j] - sum;
    }

    // Lower triangular
    for (let i = j + 1; i < n; i++) {
      let sum = 0;
      for (let k = 0; k < j; k++) {
        sum += L[i][k] * U[k][j];
      }
      if (Math.abs(U[j][j]) < 1e-10) {
        throw new Error('Zero pivot encountered');
      }
      L[i][j] = (A[i][j] - sum) / U[j][j];
    }
  }

  return { L, U };
}

/**
 * Matrix transpose
 * @param {number[][]} matrix - Input matrix
 * @returns {number[][]} - Transposed matrix
 */
export function matrixTranspose(matrix) {
  const rows = matrix.length;
  const cols = matrix[0].length;

  const result = Array(cols).fill(null).map(() => Array(rows).fill(0));

  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      result[j][i] = matrix[i][j];
    }
  }

  return result;
}

/**
 * Solve linear system Ax = b using Gaussian elimination
 * @param {number[][]} A - Coefficient matrix
 * @param {number[]} b - Right-hand side vector
 * @returns {number[]} - Solution vector x
 */
export function linearEquationSolver(A, b) {
  const n = A.length;

  // Create augmented matrix
  const augmented = A.map((row, i) => [...row, b[i]]);

  // Forward elimination
  for (let col = 0; col < n; col++) {
    // Find pivot
    let maxRow = col;
    for (let row = col + 1; row < n; row++) {
      if (Math.abs(augmented[row][col]) > Math.abs(augmented[maxRow][col])) {
        maxRow = row;
      }
    }

    // Swap rows
    [augmented[col], augmented[maxRow]] = [augmented[maxRow], augmented[col]];

    if (Math.abs(augmented[col][col]) < 1e-10) {
      throw new Error('System has no unique solution');
    }

    // Eliminate column
    for (let row = col + 1; row < n; row++) {
      const factor = augmented[row][col] / augmented[col][col];
      for (let j = col; j <= n; j++) {
        augmented[row][j] -= factor * augmented[col][j];
      }
    }
  }

  // Back substitution
  const x = Array(n).fill(0);
  for (let i = n - 1; i >= 0; i--) {
    x[i] = augmented[i][n];
    for (let j = i + 1; j < n; j++) {
      x[i] -= augmented[i][j] * x[j];
    }
    x[i] /= augmented[i][i];
  }

  return x;
}

/**
 * Create identity matrix
 * @param {number} n - Size of matrix
 * @returns {number[][]} - Identity matrix
 */
export function identityMatrix(n) {
  const result = Array(n).fill(null).map(() => Array(n).fill(0));
  for (let i = 0; i < n; i++) {
    result[i][i] = 1;
  }
  return result;
}

/**
 * Matrix addition
 * @param {number[][]} A - First matrix
 * @param {number[][]} B - Second matrix
 * @returns {number[][]} - Sum matrix A + B
 */
export function matrixAdd(A, B) {
  const rows = A.length;
  const cols = A[0].length;

  return A.map((row, i) =>
    row.map((val, j) => val + B[i][j])
  );
}

/**
 * Matrix scalar multiplication
 * @param {number[][]} matrix - Input matrix
 * @param {number} scalar - Scalar value
 * @returns {number[][]} - Scaled matrix
 */
export function matrixScalarMultiply(matrix, scalar) {
  return matrix.map(row =>
    row.map(val => val * scalar)
  );
}

/**
 * Vector magnitude (Euclidean norm)
 * @param {number[]} v - Input vector
 * @returns {number} - Magnitude
 */
export function vectorMagnitude(v) {
  return Math.sqrt(v.reduce((sum, val) => sum + val * val, 0));
}

/**
 * Normalize vector
 * @param {number[]} v - Input vector
 * @returns {number[]} - Unit vector
 */
export function vectorNormalize(v) {
  const mag = vectorMagnitude(v);
  if (mag === 0) {
    return v.map(() => 0);
  }
  return v.map(val => val / mag);
}
