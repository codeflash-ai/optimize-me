package com.optimizeme;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class CollectionUtils {

    public static <T extends Comparable<T>> List<T> mergeSorted(List<T> a, List<T> b) {
        int na = a.size();
        int nb = b.size();
        List<T> result = new ArrayList<>(na + nb);

        // Fast path for random-access lists: avoid duplicate get() calls by caching current elements
        if (a instanceof java.util.RandomAccess && b instanceof java.util.RandomAccess) {
            if (na == 0) {
                if (nb > 0) result.addAll(b);
                return result;
            }
            if (nb == 0) {
                if (na > 0) result.addAll(a);
                return result;
            }
            int i = 0, j = 0;
            T aval = a.get(0);
            T bval = b.get(0);
            while (i < na && j < nb) {
                if (aval.compareTo(bval) <= 0) {
                    result.add(aval);
                    i++;
                    if (i < na) {
                        aval = a.get(i);
                    }
                } else {
                    result.add(bval);
                    j++;
                    if (j < nb) {
                        bval = b.get(j);
                    }
                }
            }
            while (i < na) {
                result.add(a.get(i++));
            }
            while (j < nb) {
                result.add(b.get(j++));
            }
            return result;
        }

        // Generic path for non-random-access lists: use iterators to get O(n) traversal
        java.util.Iterator<T> ita = a.iterator();
        java.util.Iterator<T> itb = b.iterator();

        if (!ita.hasNext()) {
            while (itb.hasNext()) {
                result.add(itb.next());
            }
            return result;
        }
        if (!itb.hasNext()) {
            while (ita.hasNext()) {
                result.add(ita.next());
            }
            return result;
        }

        T aval = ita.next();
        T bval = itb.next();

        while (true) {
            if (aval.compareTo(bval) <= 0) {
                result.add(aval);
                if (ita.hasNext()) {
                    aval = ita.next();
                } else {
                    // drain remaining from b (including current bval)
                    result.add(bval);
                    while (itb.hasNext()) result.add(itb.next());
                    break;
                }
            } else {
                result.add(bval);
                if (itb.hasNext()) {
                    bval = itb.next();
                } else {
                    // drain remaining from a (including current aval)
                    result.add(aval);
                    while (ita.hasNext()) result.add(ita.next());
                    break;
                }
            }
        }

        return result;
    }

    public static class FrequencyCounter<T> {
        private final Map<T, Integer> counts = new HashMap<>();

        public void add(T item) {
            counts.merge(item, 1, Integer::sum);
        }

        public int getCount(T item) {
            return counts.getOrDefault(item, 0);
        }

        public T mostFrequent() {
            return counts.entrySet().stream()
                    .max(Map.Entry.comparingByValue())
                    .map(Map.Entry::getKey)
                    .orElse(null);
        }
    }
}
