import { describe, it, expect } from 'vitest';
import { pipeline, groupBy, chunk } from '../src/dataTransform';

describe('pipeline', () => {
  it('chains functions correctly', () => {
    const result = pipeline(5, (x) => x * 2, (x) => x + 1);
    expect(result).toBe(11);
  });

  it('returns value unchanged with no functions', () => {
    expect(pipeline(42)).toBe(42);
  });
});

describe('groupBy', () => {
  it('groups items by key function', () => {
    const items = [{type: 'a', val: 1}, {type: 'b', val: 2}, {type: 'a', val: 3}];
    const grouped = groupBy(items, item => item.type);
    expect(grouped['a']).toHaveLength(2);
    expect(grouped['b']).toHaveLength(1);
  });

  it('returns empty object for empty array', () => {
    const grouped = groupBy([], () => 'key');
    expect(Object.keys(grouped)).toHaveLength(0);
  });
});

describe('chunk', () => {
  it('splits array into chunks of given size', () => {
    const chunked = chunk([1, 2, 3, 4, 5], 2);
    expect(chunked).toEqual([[1, 2], [3, 4], [5]]);
  });

  it('returns single chunk when size >= array length', () => {
    const chunked = chunk([1, 2, 3], 5);
    expect(chunked).toEqual([[1, 2, 3]]);
  });
});
