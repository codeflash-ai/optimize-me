import { describe, it, expect } from 'vitest';
import { memoize } from '../src/asyncUtils.js';

describe('memoize', () => {
  it('returns correct result', () => {
    const add = (a, b) => a + b;
    const memoizedAdd = memoize(add);
    expect(memoizedAdd(1, 2)).toBe(3);
  });

  it('returns cached result on repeated call', () => {
    let callCount = 0;
    const add = (a, b) => { callCount++; return a + b; };
    const memoizedAdd = memoize(add);
    memoizedAdd(1, 2);
    memoizedAdd(1, 2);
    expect(callCount).toBe(1);
  });

  it('computes new result for different args', () => {
    const add = (a, b) => a + b;
    const memoizedAdd = memoize(add);
    expect(memoizedAdd(1, 2)).toBe(3);
    expect(memoizedAdd(3, 4)).toBe(7);
  });
});
