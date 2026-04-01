package com.optimizeme;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class CollectionUtils {

    public static <T extends Comparable<T>> List<T> mergeSorted(List<T> a, List<T> b) {
        List<T> result = new ArrayList<>(a.size() + b.size());
        int i = 0, j = 0;
        while (i < a.size() && j < b.size()) {
            if (a.get(i).compareTo(b.get(j)) <= 0) {
                result.add(a.get(i++));
            } else {
                result.add(b.get(j++));
            }
        }
        while (i < a.size()) {
            result.add(a.get(i++));
        }
        while (j < b.size()) {
            result.add(b.get(j++));
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
