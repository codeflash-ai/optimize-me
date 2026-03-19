package com.optimizeme;

import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;

public class StringProcessorTest {

    @Test
    public void testReverseWords() {
        assertEquals("world hello", StringProcessor.reverseWords("hello world"));
    }

    @Test
    public void testReverseWordsNull() {
        assertNull(StringProcessor.reverseWords(null));
    }

    @Test
    public void testCountVowels() {
        assertEquals(3, StringProcessor.countVowels("Hello World"));
    }

    @Test
    public void testIsPalindrome() {
        assertTrue(StringProcessor.isPalindrome("A man a plan a canal Panama"));
    }
}
