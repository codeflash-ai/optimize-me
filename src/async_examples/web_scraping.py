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


async def scrape_with_poor_error_handling(urls):
    """
    Has poor error handling that can crash entire scraping operation.
    Should handle individual failures gracefully.
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        for url in urls:
            # Creates tasks but doesn't handle individual failures
            task = asyncio.create_task(scrape_single_url_unsafe(session, url))
            tasks.append(task)
        
        # If any task fails, entire operation fails
        results = await asyncio.gather(*tasks)  # Should use return_exceptions=True
        
        return results


async def scrape_single_url_unsafe(session, url):
    """Helper function with no error handling"""
    async with session.get(url) as response:
        # Will raise exception on non-200 status codes
        response.raise_for_status()
        
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        
        # Assumes title always exists - will crash if not
        title = soup.find('title').text.strip()
        
        return {
            'url': url,
            'title': title,
            'status_code': response.status
        }


async def scrape_with_inefficient_rate_limiting(urls, delay=1.0):
    """
    Implements rate limiting inefficiently by adding delays to all requests.
    Should use semaphores or proper rate limiting libraries.
    """
    results = []
    
    async with aiohttp.ClientSession() as session:
        for url in urls:
            try:
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
                
                # Fixed delay regardless of server response time
                await asyncio.sleep(delay)
                
            except Exception as e:
                results.append({
                    'url': url,
                    'title': f"Error: {str(e)}",
                    'status_code': None
                })
    
    return results


async def scrape_with_memory_leaks(base_urls):
    """
    Demonstrates patterns that can lead to memory leaks in scraping.
    Accumulates too much data without proper cleanup.
    """
    all_data = []  # Grows unbounded
    
    async with aiohttp.ClientSession() as session:
        for base_url in base_urls:
            try:
                # Scrape main page
                async with session.get(base_url) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Store entire HTML content - memory inefficient
                    page_data = {
                        'url': base_url,
                        'html': html,  # Stores full HTML in memory
                        'links': []
                    }
                    
                    # Extract all links
                    for link in soup.find_all('a', href=True):
                        link_url = urljoin(base_url, link['href'])
                        
                        # Scrape each linked page too - exponential growth
                        try:
                            async with session.get(link_url) as link_response:
                                link_html = await link_response.text()
                                page_data['links'].append({
                                    'url': link_url,
                                    'html': link_html  # More full HTML stored
                                })
                        except:
                            pass  # Silently ignore errors
                    
                    all_data.append(page_data)
            
            except Exception as e:
                print(f"Error scraping {base_url}: {e}")
    
    return all_data  # Returns massive data structure


async def scrape_without_respect_for_robots_txt(urls):
    """
    Scrapes without checking robots.txt or respecting server limits.
    Should check robots.txt and implement proper politeness policies.
    """
    results = []
    
    # Creates too many concurrent connections - can overwhelm servers
    connector = aiohttp.TCPConnector(limit=100, limit_per_host=50)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        # Launches all requests at once without rate limiting
        tasks = []
        
        for url in urls:
            task = asyncio.create_task(aggressive_scrape(session, url))
            tasks.append(task)
        
        # No delay between requests - can be seen as DDoS
        results = await asyncio.gather(*tasks, return_exceptions=True)
    
    return results


async def aggressive_scrape(session, url):
    """Aggressively scrapes without politeness"""
    try:
        # No custom headers - easily detected as bot
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extracts everything possible - inefficient
            data = {
                'url': url,
                'title': soup.find('title').text if soup.find('title') else None,
                'all_text': soup.get_text(),  # Extracts all text
                'all_links': [a.get('href') for a in soup.find_all('a', href=True)],
                'all_images': [img.get('src') for img in soup.find_all('img', src=True)],
                'meta_tags': [str(meta) for meta in soup.find_all('meta')]
            }
            
            return data
            
    except Exception as e:
        return {'url': url, 'error': str(e)}


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