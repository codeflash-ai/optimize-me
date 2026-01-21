/**
 * Tests for Stats Module
 */

import {
  mean,
  std,
  variance,
  median,
  describe as describeStats,
  cosineSimilarityVectors,
  cosineSimilarity,
  cosineSimilarityTopK,
  pearsonCorrelation,
  correlation,
  pca,
  kmeansClustering,
  gradientDescent,
  linearPredict
} from '../src/stats/statistical.js';

import {
  DataFrame,
  dataframeFilter,
  groupbyMean,
  dataframeMerge,
  pivotTable,
  applyFunction,
  fillna,
  dropDuplicates,
  sortValues,
  reindex,
  melt,
  selectColumns,
  renameColumns
} from '../src/stats/dataframe.js';

describe('Statistical Functions', () => {
  describe('mean', () => {
    test('simple array', () => {
      expect(mean([1, 2, 3, 4, 5])).toBe(3);
    });

    test('single element', () => {
      expect(mean([5])).toBe(5);
    });

    test('empty array', () => {
      expect(mean([])).toBeNaN();
    });
  });

  describe('std', () => {
    test('population std', () => {
      expect(std([2, 4, 4, 4, 5, 5, 7, 9])).toBeCloseTo(2, 5);
    });

    test('sample std', () => {
      const result = std([2, 4, 4, 4, 5, 5, 7, 9], true);
      expect(result).toBeCloseTo(2.138, 2);
    });
  });

  describe('median', () => {
    test('odd length', () => {
      expect(median([1, 3, 2])).toBe(2);
    });

    test('even length', () => {
      expect(median([1, 2, 3, 4])).toBe(2.5);
    });

    test('single element', () => {
      expect(median([5])).toBe(5);
    });
  });

  describe('describeStats', () => {
    test('basic statistics', () => {
      const result = describeStats([1, 2, 3, 4, 5]);
      expect(result.count).toBe(5);
      expect(result.mean).toBe(3);
      expect(result.min).toBe(1);
      expect(result.max).toBe(5);
    });
  });

  describe('cosineSimilarityVectors', () => {
    test('identical vectors', () => {
      expect(cosineSimilarityVectors([1, 2, 3], [1, 2, 3])).toBeCloseTo(1, 5);
    });

    test('orthogonal vectors', () => {
      expect(cosineSimilarityVectors([1, 0], [0, 1])).toBeCloseTo(0, 5);
    });

    test('opposite vectors', () => {
      expect(cosineSimilarityVectors([1, 0], [-1, 0])).toBeCloseTo(-1, 5);
    });
  });

  describe('cosineSimilarity', () => {
    test('2x2 similarity matrix', () => {
      const X = [[1, 0], [0, 1]];
      const Y = [[1, 0], [0, 1]];
      const result = cosineSimilarity(X, Y);
      expect(result[0][0]).toBeCloseTo(1, 5);
      expect(result[0][1]).toBeCloseTo(0, 5);
      expect(result[1][0]).toBeCloseTo(0, 5);
      expect(result[1][1]).toBeCloseTo(1, 5);
    });
  });

  describe('cosineSimilarityTopK', () => {
    test('top 2 matches', () => {
      const X = [[1, 0, 0]];
      const Y = [[1, 0, 0], [0, 1, 0], [0.9, 0.1, 0]];
      const result = cosineSimilarityTopK(X, Y, 2);
      expect(result[0].length).toBe(2);
      expect(result[0][0].yIndex).toBe(0); // Most similar
    });
  });

  describe('pearsonCorrelation', () => {
    test('perfect positive correlation', () => {
      expect(pearsonCorrelation([1, 2, 3], [2, 4, 6])).toBeCloseTo(1, 5);
    });

    test('perfect negative correlation', () => {
      expect(pearsonCorrelation([1, 2, 3], [6, 4, 2])).toBeCloseTo(-1, 5);
    });

    test('weak correlation', () => {
      // [1, 2, 3] vs [3, 1, 2] has correlation of -0.5
      expect(pearsonCorrelation([1, 2, 3], [3, 1, 2])).toBeCloseTo(-0.5, 1);
    });
  });

  describe('pca', () => {
    test('reduces dimensions', () => {
      const X = [[1, 2], [3, 4], [5, 6], [7, 8]];
      const result = pca(X, 1);
      expect(result.components.length).toBe(1);
      expect(result.transformed[0].length).toBe(1);
    });

    test('explained variance sums to 1', () => {
      const X = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]];
      const result = pca(X, 2);
      const sum = result.explained.reduce((a, b) => a + b, 0);
      expect(sum).toBeLessThanOrEqual(1.01);
    });
  });

  describe('kmeansClustering', () => {
    test('finds correct number of clusters', () => {
      const X = [[0, 0], [0, 1], [10, 10], [10, 11]];
      const result = kmeansClustering(X, 2, 50);
      expect(result.centroids.length).toBe(2);
      expect(result.labels.length).toBe(4);
    });

    test('assigns same cluster to nearby points', () => {
      const X = [[0, 0], [0.1, 0.1], [100, 100], [100.1, 100.1]];
      const result = kmeansClustering(X, 2, 50);
      expect(result.labels[0]).toBe(result.labels[1]);
      expect(result.labels[2]).toBe(result.labels[3]);
    });
  });

  describe('gradientDescent', () => {
    test('learns simple linear relationship', () => {
      const X = [[1], [2], [3], [4], [5]];
      const y = [2, 4, 6, 8, 10]; // y = 2x
      const { weights, bias } = gradientDescent(X, y, 0.1, 1000);
      expect(weights[0]).toBeCloseTo(2, 1);
      expect(bias).toBeCloseTo(0, 1);
    });
  });

  describe('linearPredict', () => {
    test('makes predictions', () => {
      const X = [[1], [2], [3]];
      const predictions = linearPredict(X, [2], 1);
      expect(predictions[0]).toBeCloseTo(3, 5);
      expect(predictions[1]).toBeCloseTo(5, 5);
      expect(predictions[2]).toBeCloseTo(7, 5);
    });
  });
});

describe('DataFrame Operations', () => {
  describe('DataFrame class', () => {
    test('creates from array of objects', () => {
      const df = new DataFrame([{ a: 1, b: 2 }, { a: 3, b: 4 }]);
      expect(df.length).toBe(2);
      expect(df.columns).toEqual(['a', 'b']);
    });

    test('creates from object of arrays', () => {
      const df = new DataFrame({ a: [1, 3], b: [2, 4] });
      expect(df.length).toBe(2);
    });
  });

  describe('dataframeFilter', () => {
    test('filters by column value', () => {
      const df = [{ a: 1, b: 2 }, { a: 1, b: 3 }, { a: 2, b: 4 }];
      const result = dataframeFilter(df, 'a', 1);
      expect(result.length).toBe(2);
    });

    test('returns empty for no matches', () => {
      const df = [{ a: 1 }, { a: 2 }];
      expect(dataframeFilter(df, 'a', 3)).toEqual([]);
    });
  });

  describe('groupbyMean', () => {
    test('computes group means', () => {
      const df = [
        { group: 'A', value: 10 },
        { group: 'A', value: 20 },
        { group: 'B', value: 30 }
      ];
      const result = groupbyMean(df, 'group', 'value');
      expect(result['A']).toBe(15);
      expect(result['B']).toBe(30);
    });
  });

  describe('dataframeMerge', () => {
    test('inner join', () => {
      const left = [{ id: 1, x: 'a' }, { id: 2, x: 'b' }];
      const right = [{ id: 1, y: 'c' }, { id: 3, y: 'd' }];
      const result = dataframeMerge(left, right, 'id', 'id');
      expect(result.length).toBe(1);
      expect(result[0].x).toBe('a');
      expect(result[0].y).toBe('c');
    });
  });

  describe('pivotTable', () => {
    test('sum aggregation', () => {
      const df = [
        { region: 'North', product: 'A', sales: 100 },
        { region: 'North', product: 'A', sales: 50 },
        { region: 'South', product: 'B', sales: 200 }
      ];
      const result = pivotTable(df, 'region', 'product', 'sales', 'sum');
      expect(result['North']['A']).toBe(150);
      expect(result['South']['B']).toBe(200);
    });
  });

  describe('applyFunction', () => {
    test('applies function to column', () => {
      const df = [{ a: 1 }, { a: 2 }];
      const result = applyFunction(df, 'a', x => x * 2);
      expect(result[0].a).toBe(2);
      expect(result[1].a).toBe(4);
    });
  });

  describe('fillna', () => {
    test('fills null values', () => {
      const df = [{ a: 1 }, { a: null }, { a: 3 }];
      const result = fillna(df, 'a', 0);
      expect(result[1].a).toBe(0);
    });

    test('fills undefined values', () => {
      const df = [{ a: 1 }, { a: undefined }];
      const result = fillna(df, 'a', -1);
      expect(result[1].a).toBe(-1);
    });
  });

  describe('dropDuplicates', () => {
    test('removes duplicates', () => {
      const df = [{ a: 1, b: 2 }, { a: 1, b: 2 }, { a: 1, b: 3 }];
      const result = dropDuplicates(df);
      expect(result.length).toBe(2);
    });

    test('subset columns', () => {
      const df = [{ a: 1, b: 2 }, { a: 1, b: 3 }];
      const result = dropDuplicates(df, ['a']);
      expect(result.length).toBe(1);
    });
  });

  describe('sortValues', () => {
    test('ascending sort', () => {
      const df = [{ a: 3 }, { a: 1 }, { a: 2 }];
      const result = sortValues(df, 'a', true);
      expect(result[0].a).toBe(1);
      expect(result[1].a).toBe(2);
      expect(result[2].a).toBe(3);
    });

    test('descending sort', () => {
      const df = [{ a: 1 }, { a: 3 }, { a: 2 }];
      const result = sortValues(df, 'a', false);
      expect(result[0].a).toBe(3);
      expect(result[1].a).toBe(2);
      expect(result[2].a).toBe(1);
    });
  });

  describe('melt', () => {
    test('unpivots dataframe', () => {
      const df = [{ id: 1, A: 10, B: 20 }];
      const result = melt(df, ['id'], ['A', 'B']);
      expect(result.length).toBe(2);
      expect(result[0].variable).toBe('A');
      expect(result[0].value).toBe(10);
    });
  });

  describe('selectColumns', () => {
    test('selects specified columns', () => {
      const df = [{ a: 1, b: 2, c: 3 }];
      const result = selectColumns(df, ['a', 'c']);
      expect(result[0]).toEqual({ a: 1, c: 3 });
    });
  });

  describe('renameColumns', () => {
    test('renames columns', () => {
      const df = [{ old_name: 1 }];
      const result = renameColumns(df, { old_name: 'new_name' });
      expect(result[0].new_name).toBe(1);
      expect(result[0].old_name).toBeUndefined();
    });
  });
});
