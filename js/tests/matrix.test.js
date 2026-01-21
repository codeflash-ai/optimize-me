/**
 * Tests for Matrix Module
 */

import {
  matrixMultiply,
  dotProduct,
  matrixInverse,
  matrixDeterminant,
  luDecomposition,
  matrixTranspose,
  linearEquationSolver,
  identityMatrix,
  matrixAdd,
  matrixScalarMultiply,
  vectorMagnitude,
  vectorNormalize
} from '../src/matrix/matrixOperations.js';

import {
  convolution1d,
  fft,
  createGaussianKernel,
  convolution2d,
  gaussianBlur,
  imageRotation,
  histogramEqualization,
  rollingMean
} from '../src/matrix/signalProcessing.js';

describe('Matrix Operations', () => {
  describe('matrixMultiply', () => {
    test('2x2 matrices', () => {
      const A = [[1, 2], [3, 4]];
      const B = [[5, 6], [7, 8]];
      expect(matrixMultiply(A, B)).toEqual([[19, 22], [43, 50]]);
    });

    test('identity multiplication', () => {
      const A = [[1, 2], [3, 4]];
      const I = [[1, 0], [0, 1]];
      expect(matrixMultiply(A, I)).toEqual(A);
    });

    test('non-square matrices', () => {
      const A = [[1, 2, 3], [4, 5, 6]];
      const B = [[7, 8], [9, 10], [11, 12]];
      expect(matrixMultiply(A, B)).toEqual([[58, 64], [139, 154]]);
    });
  });

  describe('dotProduct', () => {
    test('simple vectors', () => {
      expect(dotProduct([1, 2, 3], [4, 5, 6])).toBe(32);
    });

    test('zero vectors', () => {
      expect(dotProduct([0, 0], [1, 2])).toBe(0);
    });

    test('unit vectors', () => {
      expect(dotProduct([1, 0], [0, 1])).toBe(0);
    });

    test('throws for different lengths', () => {
      expect(() => dotProduct([1, 2], [1, 2, 3])).toThrow();
    });
  });

  describe('matrixDeterminant', () => {
    test('1x1 matrix', () => {
      expect(matrixDeterminant([[5]])).toBe(5);
    });

    test('2x2 matrix', () => {
      expect(matrixDeterminant([[1, 2], [3, 4]])).toBe(-2);
    });

    test('3x3 matrix', () => {
      const A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
      expect(matrixDeterminant(A)).toBeCloseTo(0, 5);
    });

    test('identity matrix', () => {
      const I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
      expect(matrixDeterminant(I)).toBe(1);
    });
  });

  describe('matrixInverse', () => {
    test('2x2 matrix', () => {
      const A = [[4, 7], [2, 6]];
      const inv = matrixInverse(A);
      expect(inv[0][0]).toBeCloseTo(0.6, 5);
      expect(inv[0][1]).toBeCloseTo(-0.7, 5);
      expect(inv[1][0]).toBeCloseTo(-0.2, 5);
      expect(inv[1][1]).toBeCloseTo(0.4, 5);
    });

    test('identity inverse is identity', () => {
      const I = [[1, 0], [0, 1]];
      const inv = matrixInverse(I);
      expect(inv[0][0]).toBeCloseTo(1, 5);
      expect(inv[0][1]).toBeCloseTo(0, 5);
      expect(inv[1][0]).toBeCloseTo(0, 5);
      expect(inv[1][1]).toBeCloseTo(1, 5);
    });

    test('throws for singular matrix', () => {
      const A = [[1, 2], [2, 4]];
      expect(() => matrixInverse(A)).toThrow();
    });
  });

  describe('luDecomposition', () => {
    test('2x2 matrix', () => {
      const A = [[4, 3], [6, 3]];
      const { L, U } = luDecomposition(A);

      // Verify L is lower triangular with 1s on diagonal
      expect(L[0][0]).toBe(1);
      expect(L[1][1]).toBe(1);
      expect(L[0][1]).toBe(0);

      // Verify L * U = A
      const product = matrixMultiply(L, U);
      expect(product[0][0]).toBeCloseTo(A[0][0], 5);
      expect(product[0][1]).toBeCloseTo(A[0][1], 5);
      expect(product[1][0]).toBeCloseTo(A[1][0], 5);
      expect(product[1][1]).toBeCloseTo(A[1][1], 5);
    });
  });

  describe('matrixTranspose', () => {
    test('square matrix', () => {
      expect(matrixTranspose([[1, 2], [3, 4]])).toEqual([[1, 3], [2, 4]]);
    });

    test('non-square matrix', () => {
      expect(matrixTranspose([[1, 2, 3], [4, 5, 6]])).toEqual([[1, 4], [2, 5], [3, 6]]);
    });
  });

  describe('linearEquationSolver', () => {
    test('2x2 system', () => {
      const A = [[2, 1], [1, 3]];
      const b = [4, 5];
      const x = linearEquationSolver(A, b);
      expect(x[0]).toBeCloseTo(1.4, 5);
      expect(x[1]).toBeCloseTo(1.2, 5);
    });

    test('3x3 system', () => {
      const A = [[1, 1, 1], [0, 2, 5], [2, 5, -1]];
      const b = [6, -4, 27];
      const x = linearEquationSolver(A, b);
      expect(x[0]).toBeCloseTo(5, 5);
      expect(x[1]).toBeCloseTo(3, 5);
      expect(x[2]).toBeCloseTo(-2, 5);
    });
  });

  describe('identityMatrix', () => {
    test('2x2 identity', () => {
      expect(identityMatrix(2)).toEqual([[1, 0], [0, 1]]);
    });

    test('3x3 identity', () => {
      expect(identityMatrix(3)).toEqual([[1, 0, 0], [0, 1, 0], [0, 0, 1]]);
    });
  });

  describe('matrixAdd', () => {
    test('2x2 matrices', () => {
      expect(matrixAdd([[1, 2], [3, 4]], [[5, 6], [7, 8]])).toEqual([[6, 8], [10, 12]]);
    });
  });

  describe('matrixScalarMultiply', () => {
    test('multiply by 2', () => {
      expect(matrixScalarMultiply([[1, 2], [3, 4]], 2)).toEqual([[2, 4], [6, 8]]);
    });

    test('multiply by 0', () => {
      expect(matrixScalarMultiply([[1, 2], [3, 4]], 0)).toEqual([[0, 0], [0, 0]]);
    });
  });

  describe('vectorMagnitude', () => {
    test('3D vector', () => {
      expect(vectorMagnitude([3, 4, 0])).toBe(5);
    });

    test('unit vector', () => {
      expect(vectorMagnitude([1, 0, 0])).toBe(1);
    });
  });

  describe('vectorNormalize', () => {
    test('simple vector', () => {
      const normalized = vectorNormalize([3, 4, 0]);
      expect(normalized[0]).toBeCloseTo(0.6, 5);
      expect(normalized[1]).toBeCloseTo(0.8, 5);
      expect(normalized[2]).toBeCloseTo(0, 5);
    });

    test('zero vector', () => {
      expect(vectorNormalize([0, 0, 0])).toEqual([0, 0, 0]);
    });
  });
});

describe('Signal Processing', () => {
  describe('convolution1d', () => {
    test('simple convolution', () => {
      const signal = [1, 2, 3, 4, 5];
      const kernel = [1, 0, -1];
      const result = convolution1d(signal, kernel);
      expect(result.length).toBe(7);
    });

    test('identity kernel', () => {
      const signal = [1, 2, 3];
      const kernel = [1];
      expect(convolution1d(signal, kernel)).toEqual([1, 2, 3]);
    });
  });

  describe('fft', () => {
    test('power of 2 length', () => {
      const x = [1, 0, 0, 0];
      const result = fft(x);
      expect(result.real.length).toBe(4);
      expect(result.imag.length).toBe(4);
    });

    test('constant signal', () => {
      const x = [1, 1, 1, 1];
      const result = fft(x);
      expect(result.real[0]).toBeCloseTo(4, 5);
    });

    test('throws for non-power of 2', () => {
      expect(() => fft([1, 2, 3])).toThrow();
    });
  });

  describe('createGaussianKernel', () => {
    test('3x3 kernel', () => {
      const kernel = createGaussianKernel(3, 1.0);
      expect(kernel.length).toBe(3);
      expect(kernel[0].length).toBe(3);

      // Sum should be approximately 1
      const sum = kernel.flat().reduce((a, b) => a + b, 0);
      expect(sum).toBeCloseTo(1, 5);
    });

    test('center is maximum', () => {
      const kernel = createGaussianKernel(5, 1.0);
      const center = kernel[2][2];
      expect(center).toBeGreaterThan(kernel[0][0]);
      expect(center).toBeGreaterThan(kernel[0][4]);
    });
  });

  describe('gaussianBlur', () => {
    test('preserves image dimensions', () => {
      const image = [[100, 150, 200], [120, 170, 220], [140, 190, 240]];
      const blurred = gaussianBlur(image, 3, 1.0);
      expect(blurred.length).toBe(3);
      expect(blurred[0].length).toBe(3);
    });
  });

  describe('imageRotation', () => {
    test('360 degree rotation returns similar image', () => {
      const image = [[1, 2], [3, 4]];
      const rotated = imageRotation(image, 360);
      expect(rotated.length).toBe(2);
      expect(rotated[0].length).toBe(2);
    });

    test('preserves dimensions', () => {
      const image = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
      const rotated = imageRotation(image, 45);
      expect(rotated.length).toBe(3);
      expect(rotated[0].length).toBe(3);
    });
  });

  describe('histogramEqualization', () => {
    test('preserves value range', () => {
      const image = [[50, 100], [150, 200]];
      const equalized = histogramEqualization(image);
      for (const row of equalized) {
        for (const val of row) {
          expect(val).toBeGreaterThanOrEqual(0);
          expect(val).toBeLessThanOrEqual(255);
        }
      }
    });
  });

  describe('rollingMean', () => {
    test('window of 3', () => {
      const series = [1, 2, 3, 4, 5];
      const result = rollingMean(series, 3);
      expect(result.length).toBe(5);
      expect(result[0]).toBeNaN();
      expect(result[1]).toBeNaN();
      expect(result[2]).toBeCloseTo(2, 5);
      expect(result[3]).toBeCloseTo(3, 5);
      expect(result[4]).toBeCloseTo(4, 5);
    });

    test('window of 1', () => {
      const series = [1, 2, 3];
      const result = rollingMean(series, 1);
      expect(result).toEqual([1, 2, 3]);
    });
  });
});
