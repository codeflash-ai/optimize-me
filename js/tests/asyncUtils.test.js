const { memoize } = require('../src/asyncUtils');

// Simple test runner
function assert(condition, message) {
  if (!condition) throw new Error('Assertion failed: ' + message);
}

// Test memoize
const add = (a, b) => a + b;
const memoizedAdd = memoize(add);
assert(memoizedAdd(1, 2) === 3, 'memoize returns correct result');
assert(memoizedAdd(1, 2) === 3, 'memoize returns cached result');

console.log('asyncUtils tests passed');
