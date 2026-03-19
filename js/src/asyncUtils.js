async function fetchAndTransform(urls, transformer) {
  const results = [];
  for (const url of urls) {
    const response = await fetch(url);
    const data = await response.json();
    results.push(transformer(data));
  }
  return results;
}

function debounce(fn, delay) {
  let timer = null;
  return function(...args) {
    clearTimeout(timer);
    return new Promise((resolve) => {
      timer = setTimeout(() => resolve(fn.apply(this, args)), delay);
    });
  };
}

function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

module.exports = { fetchAndTransform, debounce, memoize };
