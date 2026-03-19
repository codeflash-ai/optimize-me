import { pipeline, groupBy, chunk } from '../src/dataTransform';

function assert(condition: boolean, message: string): void {
  if (!condition) throw new Error('Assertion failed: ' + message);
}

// Test pipeline
const result = pipeline(5, (x) => x * 2, (x) => x + 1);
assert(result === 11, 'pipeline chains functions correctly');

// Test groupBy
const items = [{type: 'a', val: 1}, {type: 'b', val: 2}, {type: 'a', val: 3}];
const grouped = groupBy(items, item => item.type);
assert(grouped['a'].length === 2, 'groupBy groups correctly');

// Test chunk
const chunked = chunk([1,2,3,4,5], 2);
assert(chunked.length === 3, 'chunk splits correctly');
assert(chunked[0].length === 2, 'chunk size correct');

console.log('dataTransform tests passed');
