interface Transformer<TInput, TOutput> {
  transform(input: TInput): TOutput;
  name: string;
}

function pipeline<T>(value: T, ...fns: Array<(arg: T) => T>): T {
  let result = value;
  const len = fns.length;
  for (let i = 0; i < len; i++) {
    result = fns[i](result);
  }
  return result;
}

function groupBy<T>(items: T[], keyFn: (item: T) => string): Record<string, T[]> {
  const result: Record<string, T[]> = {};
  for (const item of items) {
    const key = keyFn(item);
    if (!result[key]) result[key] = [];
    result[key].push(item);
  }
  return result;
}

function chunk<T>(array: T[], size: number): T[][] {
  const chunks: T[][] = [];
  for (let i = 0; i < array.length; i += size) {
    chunks.push(array.slice(i, i + size));
  }
  return chunks;
}

export { Transformer, pipeline, groupBy, chunk };
