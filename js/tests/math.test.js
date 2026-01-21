/**
 * Tests for Math Module
 */

import {
  gcdRecursive,
  lcm,
  isPrime,
  sieveOfEratosthenes,
  monteCarloPi,
  newtonRaphsonSqrt,
  bisectionMethod,
  lagrangeInterpolation,
  factorial,
  power
} from '../src/math/computation.js';

describe('GCD and LCM', () => {
  describe('gcdRecursive', () => {
    test('gcd(48, 18) = 6', () => {
      expect(gcdRecursive(48, 18)).toBe(6);
    });

    test('gcd(0, 5) = 5', () => {
      expect(gcdRecursive(0, 5)).toBe(5);
    });

    test('gcd(5, 0) = 5', () => {
      expect(gcdRecursive(5, 0)).toBe(5);
    });

    test('gcd with negative numbers', () => {
      expect(gcdRecursive(-48, 18)).toBe(6);
    });

    test('coprime numbers', () => {
      expect(gcdRecursive(17, 13)).toBe(1);
    });
  });

  describe('lcm', () => {
    test('lcm(4, 6) = 12', () => {
      expect(lcm(4, 6)).toBe(12);
    });

    test('lcm(3, 5) = 15', () => {
      expect(lcm(3, 5)).toBe(15);
    });

    test('lcm(12, 18) = 36', () => {
      expect(lcm(12, 18)).toBe(36);
    });
  });
});

describe('Prime Numbers', () => {
  describe('isPrime', () => {
    test('2 is prime', () => {
      expect(isPrime(2)).toBe(true);
    });

    test('3 is prime', () => {
      expect(isPrime(3)).toBe(true);
    });

    test('4 is not prime', () => {
      expect(isPrime(4)).toBe(false);
    });

    test('17 is prime', () => {
      expect(isPrime(17)).toBe(true);
    });

    test('1 is not prime', () => {
      expect(isPrime(1)).toBe(false);
    });

    test('0 is not prime', () => {
      expect(isPrime(0)).toBe(false);
    });

    test('negative numbers are not prime', () => {
      expect(isPrime(-5)).toBe(false);
    });

    test('97 is prime', () => {
      expect(isPrime(97)).toBe(true);
    });
  });

  describe('sieveOfEratosthenes', () => {
    test('primes up to 10', () => {
      expect(sieveOfEratosthenes(10)).toEqual([2, 3, 5, 7]);
    });

    test('primes up to 30', () => {
      expect(sieveOfEratosthenes(30)).toEqual([2, 3, 5, 7, 11, 13, 17, 19, 23, 29]);
    });

    test('n = 2', () => {
      expect(sieveOfEratosthenes(2)).toEqual([2]);
    });

    test('n = 1', () => {
      expect(sieveOfEratosthenes(1)).toEqual([]);
    });

    test('n = 0', () => {
      expect(sieveOfEratosthenes(0)).toEqual([]);
    });
  });
});

describe('Numerical Methods', () => {
  describe('monteCarloPi', () => {
    test('estimation is in reasonable range', () => {
      const pi = monteCarloPi(10000);
      expect(pi).toBeGreaterThan(2.5);
      expect(pi).toBeLessThan(4.0);
    });
  });

  describe('newtonRaphsonSqrt', () => {
    test('sqrt(4) ≈ 2', () => {
      expect(newtonRaphsonSqrt(4)).toBeCloseTo(2, 5);
    });

    test('sqrt(9) ≈ 3', () => {
      expect(newtonRaphsonSqrt(9)).toBeCloseTo(3, 5);
    });

    test('sqrt(2) ≈ 1.414', () => {
      expect(newtonRaphsonSqrt(2)).toBeCloseTo(1.41421356, 5);
    });

    test('sqrt(0) = 0', () => {
      expect(newtonRaphsonSqrt(0)).toBe(0);
    });

    test('throws for negative input', () => {
      expect(() => newtonRaphsonSqrt(-1)).toThrow();
    });
  });

  describe('bisectionMethod', () => {
    test('find root of x^2 - 4', () => {
      const f = x => x * x - 4;
      expect(bisectionMethod(f, 0, 3)).toBeCloseTo(2, 5);
    });

    test('find root of x - 5', () => {
      const f = x => x - 5;
      expect(bisectionMethod(f, 0, 10)).toBeCloseTo(5, 5);
    });

    test('throws when signs are same', () => {
      const f = x => x * x + 1;
      expect(() => bisectionMethod(f, 0, 10)).toThrow();
    });
  });

  describe('lagrangeInterpolation', () => {
    test('linear interpolation', () => {
      const points = [[0, 0], [2, 4]];
      expect(lagrangeInterpolation(points, 1)).toBeCloseTo(2, 5);
    });

    test('quadratic interpolation', () => {
      const points = [[0, 0], [1, 1], [2, 4]];
      expect(lagrangeInterpolation(points, 3)).toBeCloseTo(9, 5);
    });

    test('passes through given points', () => {
      const points = [[1, 2], [3, 4], [5, 6]];
      expect(lagrangeInterpolation(points, 1)).toBeCloseTo(2, 5);
      expect(lagrangeInterpolation(points, 3)).toBeCloseTo(4, 5);
    });
  });
});

describe('Basic Math Functions', () => {
  describe('factorial', () => {
    test('0! = 1', () => {
      expect(factorial(0)).toBe(1);
    });

    test('1! = 1', () => {
      expect(factorial(1)).toBe(1);
    });

    test('5! = 120', () => {
      expect(factorial(5)).toBe(120);
    });

    test('10! = 3628800', () => {
      expect(factorial(10)).toBe(3628800);
    });

    test('throws for negative', () => {
      expect(() => factorial(-1)).toThrow();
    });
  });

  describe('power', () => {
    test('2^3 = 8', () => {
      expect(power(2, 3)).toBe(8);
    });

    test('2^0 = 1', () => {
      expect(power(2, 0)).toBe(1);
    });

    test('5^2 = 25', () => {
      expect(power(5, 2)).toBe(25);
    });

    test('2^-1 = 0.5', () => {
      expect(power(2, -1)).toBeCloseTo(0.5, 5);
    });

    test('3^-2 = 1/9', () => {
      expect(power(3, -2)).toBeCloseTo(1/9, 5);
    });
  });
});
