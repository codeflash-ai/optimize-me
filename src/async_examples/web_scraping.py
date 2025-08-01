"""
Inefficient async web scraping patterns.
These examples show common mistakes when scraping websites asynchronously.
"""

import asyncio
import aiohttp
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import random


async def scrape_urls_sequentially(urls):
    """
    Scrapes URLs one by one, defeating the purpose of async.
    Should use concurrent requests with aiohttp.
    """
    results = []
    
    for url in urls:
        try:
            # Using synchronous requests in async function - blocks event loop
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.find('title')
            title_text = title.text.strip() if title else "No title"
            
            results.append({
                'url': url,
                'title': title_text,
                'status_code': response.status_code
            })
            
            # Blocking sleep instead of asyncio.sleep
            time.sleep(1)  # Rate limiting done wrong
            
        except Exception as e:
            results.append({
                'url': url,
                'title': f"Error: {str(e)}",
                'status_code': None
            })
    
    return results


async def scrape_with_session_misuse(urls):
    """
    Creates new session for each request instead of reusing.
    Should create one session and reuse it for all requests.
    """
    results = []
    
    for url in urls:
        try:
            # Creates new session for each request - very inefficient
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    title = soup.find('title')
                    title_text = title.text.strip() if title else "No title"
                    
                    results.append({
                        'url': url,
                        'title': title_text,
                        'status_code': response.status
                    })
        
        except Exception as e:
            results.append({
                'url': url,
                'title': f"Error: {str(e)}",
                'status_code': None
            })
    
    return results





async def parse_html_inefficiently(html_content_list):
    """
    Parses HTML content inefficiently in the main thread.
    Should use asyncio.to_thread for CPU-intensive parsing.
    """
    results = []
    
    for html in html_content_list:
        # CPU-intensive parsing blocks event loop
        soup = BeautifulSoup(html, 'html.parser')
        
        # Inefficient text processing
        all_text = soup.get_text()
        words = all_text.split()
        
        # Blocking operations
        word_count = len(words)
        unique_words = len(set(words))  # CPU-intensive for large texts
        
        # More blocking text analysis
        long_words = [word for word in words if len(word) > 10]
        
        results.append({
            'word_count': word_count,
            'unique_words': unique_words,
            'long_words': long_words[:10]  # Keep only first 10
        })
        
        # Simulates more processing
        time.sleep(0.1)  # Should use asyncio.sleep or avoid entirely
    
    return results


if __name__ == "__main__":
    async def main():
        print("Running inefficient web scraping examples...")
        
        # Test URLs (using example.com to be safe)
        test_urls = [
            "http://example.com",
            "https://httpbin.org/delay/1",
            "https://httpbin.org/status/200",
            "https://httpbin.org/html",
            "https://httpbin.org/json"
        ]
        
        # Example 1: Sequential scraping
        start_time = time.time()
        results = await scrape_urls_sequentially(test_urls[:2])  # Limit to avoid delays
        print(f"Sequential scraping took: {time.time() - start_time:.2f}s")
        
        # Example 2: Session misuse
        start_time = time.time()
        results = await scrape_with_session_misuse(test_urls[:3])
        print(f"Session misuse took: {time.time() - start_time:.2f}s")
        
        # Example 3: Poor rate limiting
        start_time = time.time()
        results = await scrape_with_inefficient_rate_limiting(test_urls[:3], 0.5)
        print(f"Poor rate limiting took: {time.time() - start_time:.2f}s")
    
    asyncio.run(main())