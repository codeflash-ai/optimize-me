/**
 * DataFrame-like Operations
 * JavaScript equivalents of Pandas DataFrame operations
 */

/**
 * Simple DataFrame class for tabular data operations
 */
export class DataFrame {
  constructor(data) {
    if (Array.isArray(data)) {
      // Array of objects format
      this.data = data;
      this.columns = data.length > 0 ? Object.keys(data[0]) : [];
    } else {
      // Object of arrays format
      const columns = Object.keys(data);
      const length = columns.length > 0 ? data[columns[0]].length : 0;
      this.data = [];
      for (let i = 0; i < length; i++) {
        const row = {};
        for (const col of columns) {
          row[col] = data[col][i];
        }
        this.data.push(row);
      }
      this.columns = columns;
    }
  }

  get length() {
    return this.data.length;
  }

  toArray() {
    return this.data;
  }

  toObject() {
    const result = {};
    for (const col of this.columns) {
      result[col] = this.data.map(row => row[col]);
    }
    return result;
  }
}

/**
 * Filter DataFrame rows by column value
 * @param {Object[]} df - Array of row objects
 * @param {string} column - Column name
 * @param {*} value - Value to filter by
 * @returns {Object[]} - Filtered rows
 */
export function dataframeFilter(df, column, value) {
  const result = [];

  for (const row of df) {
    if (row[column] === value) {
      result.push({ ...row });
    }
  }

  return result;
}

/**
 * Group by and compute mean
 * @param {Object[]} df - Array of row objects
 * @param {string} groupCol - Column to group by
 * @param {string} valueCol - Column to aggregate
 * @returns {Object} - Group to mean mapping
 */
export function groupbyMean(df, groupCol, valueCol) {
  const groups = {};

  for (const row of df) {
    const key = row[groupCol];
    if (!groups[key]) {
      groups[key] = { sum: 0, count: 0 };
    }
    groups[key].sum += row[valueCol];
    groups[key].count++;
  }

  const result = {};
  for (const [key, { sum, count }] of Object.entries(groups)) {
    result[key] = sum / count;
  }

  return result;
}

/**
 * Merge two dataframes
 * @param {Object[]} left - Left dataframe
 * @param {Object[]} right - Right dataframe
 * @param {string} leftOn - Left join column
 * @param {string} rightOn - Right join column
 * @returns {Object[]} - Merged dataframe
 */
export function dataframeMerge(left, right, leftOn, rightOn) {
  const result = [];

  for (const leftRow of left) {
    for (const rightRow of right) {
      if (leftRow[leftOn] === rightRow[rightOn]) {
        const merged = { ...leftRow };
        for (const [key, value] of Object.entries(rightRow)) {
          if (key !== rightOn) {
            merged[key] = value;
          }
        }
        result.push(merged);
      }
    }
  }

  return result;
}

/**
 * Create pivot table
 * @param {Object[]} df - Array of row objects
 * @param {string} index - Index column
 * @param {string} columns - Column to pivot
 * @param {string} values - Values column
 * @param {string} aggfunc - Aggregation function ('sum', 'mean', 'count')
 * @returns {Object} - Pivot table as nested object
 */
export function pivotTable(df, index, columns, values, aggfunc = 'sum') {
  const pivot = {};
  const counts = {};

  for (const row of df) {
    const idxVal = row[index];
    const colVal = row[columns];
    const val = row[values];

    if (!pivot[idxVal]) {
      pivot[idxVal] = {};
      counts[idxVal] = {};
    }
    if (pivot[idxVal][colVal] === undefined) {
      pivot[idxVal][colVal] = 0;
      counts[idxVal][colVal] = 0;
    }

    pivot[idxVal][colVal] += val;
    counts[idxVal][colVal]++;
  }

  if (aggfunc === 'mean') {
    for (const idx of Object.keys(pivot)) {
      for (const col of Object.keys(pivot[idx])) {
        pivot[idx][col] /= counts[idx][col];
      }
    }
  } else if (aggfunc === 'count') {
    return counts;
  }

  return pivot;
}

/**
 * Apply function to column
 * @param {Object[]} df - Array of row objects
 * @param {string} column - Column to apply to
 * @param {Function} func - Function to apply
 * @returns {Object[]} - DataFrame with transformed column
 */
export function applyFunction(df, column, func) {
  return df.map(row => ({
    ...row,
    [column]: func(row[column])
  }));
}

/**
 * Fill missing values
 * @param {Object[]} df - Array of row objects
 * @param {string} column - Column to fill
 * @param {*} value - Fill value
 * @returns {Object[]} - DataFrame with filled values
 */
export function fillna(df, column, value) {
  return df.map(row => ({
    ...row,
    [column]: row[column] === null || row[column] === undefined ? value : row[column]
  }));
}

/**
 * Drop duplicate rows
 * @param {Object[]} df - Array of row objects
 * @param {string[]} subset - Columns to check for duplicates
 * @returns {Object[]} - DataFrame without duplicates
 */
export function dropDuplicates(df, subset = null) {
  const seen = new Set();
  const result = [];

  for (const row of df) {
    const key = subset
      ? subset.map(col => JSON.stringify(row[col])).join('|')
      : JSON.stringify(row);

    if (!seen.has(key)) {
      seen.add(key);
      result.push({ ...row });
    }
  }

  return result;
}

/**
 * Sort dataframe by column (bubble sort - intentionally inefficient)
 * @param {Object[]} df - Array of row objects
 * @param {string} by - Column to sort by
 * @param {boolean} ascending - Sort order
 * @returns {Object[]} - Sorted dataframe
 */
export function sortValues(df, by, ascending = true) {
  const result = df.map(row => ({ ...row }));
  const n = result.length;

  // Bubble sort (intentionally inefficient like Python version)
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n - i - 1; j++) {
      const shouldSwap = ascending
        ? result[j][by] > result[j + 1][by]
        : result[j][by] < result[j + 1][by];

      if (shouldSwap) {
        [result[j], result[j + 1]] = [result[j + 1], result[j]];
      }
    }
  }

  return result;
}

/**
 * Reindex dataframe
 * @param {Object[]} df - Array of row objects
 * @param {*[]} newIndex - New index values
 * @returns {Object[]} - Reindexed dataframe
 */
export function reindex(df, newIndex) {
  const columns = df.length > 0 ? Object.keys(df[0]) : [];
  const result = [];

  for (let i = 0; i < newIndex.length; i++) {
    if (i < df.length) {
      result.push({ ...df[i], _index: newIndex[i] });
    } else {
      const row = { _index: newIndex[i] };
      for (const col of columns) {
        row[col] = null;
      }
      result.push(row);
    }
  }

  return result;
}

/**
 * Melt (unpivot) dataframe
 * @param {Object[]} df - Array of row objects
 * @param {string[]} idVars - ID variables
 * @param {string[]} valueVars - Value variables to unpivot
 * @returns {Object[]} - Melted dataframe
 */
export function melt(df, idVars, valueVars) {
  const result = [];

  for (const row of df) {
    for (const valueVar of valueVars) {
      const newRow = { variable: valueVar, value: row[valueVar] };
      for (const idVar of idVars) {
        newRow[idVar] = row[idVar];
      }
      result.push(newRow);
    }
  }

  return result;
}

/**
 * Select columns from dataframe
 * @param {Object[]} df - Array of row objects
 * @param {string[]} columns - Columns to select
 * @returns {Object[]} - Dataframe with selected columns
 */
export function selectColumns(df, columns) {
  return df.map(row => {
    const newRow = {};
    for (const col of columns) {
      newRow[col] = row[col];
    }
    return newRow;
  });
}

/**
 * Rename columns
 * @param {Object[]} df - Array of row objects
 * @param {Object} mapping - Old name to new name mapping
 * @returns {Object[]} - Dataframe with renamed columns
 */
export function renameColumns(df, mapping) {
  return df.map(row => {
    const newRow = {};
    for (const [key, value] of Object.entries(row)) {
      const newKey = mapping[key] || key;
      newRow[newKey] = value;
    }
    return newRow;
  });
}
