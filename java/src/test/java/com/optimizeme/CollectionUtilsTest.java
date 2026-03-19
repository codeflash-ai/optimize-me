package com.optimizeme;

import org.junit.Test;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import static org.junit.Assert.assertEquals;

public class CollectionUtilsTest {

    @Test
    public void testMergeSortedIntegers() {
        List<Integer> a = Arrays.asList(1, 3, 5);
        List<Integer> b = Arrays.asList(2, 4, 6);
        List<Integer> expected = Arrays.asList(1, 2, 3, 4, 5, 6);
        assertEquals(expected, CollectionUtils.mergeSorted(a, b));
    }

    @Test
    public void testMergeSortedEmptyList() {
        List<Integer> a = Collections.emptyList();
        List<Integer> b = Arrays.asList(1, 2, 3);
        List<Integer> expected = Arrays.asList(1, 2, 3);
        assertEquals(expected, CollectionUtils.mergeSorted(a, b));
    }

    @Test
    public void testFrequencyCounterBasic() {
        CollectionUtils.FrequencyCounter<String> counter = new CollectionUtils.FrequencyCounter<>();
        counter.add("a");
        counter.add("a");
        counter.add("a");
        counter.add("b");
        assertEquals(3, counter.getCount("a"));
        assertEquals("a", counter.mostFrequent());
    }
}
