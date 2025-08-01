"""
Inefficient async database operations.
These examples show poor patterns when working with databases in async code.
"""

import asyncio
import aiosqlite
import time
from typing import List, Dict, Any


class InefficientDatabaseManager:
    """
    Database manager with multiple inefficient async patterns.
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    async def setup_database(self):
        """Sets up database with inefficient sequential operations"""
        # Opens and closes connection multiple times unnecessarily
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                )
            ''')
            await db.commit()
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    title TEXT NOT NULL,
                    content TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            await db.commit()
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts (user_id)
            ''')
            await db.commit()
    
    async def insert_users_sequentially(self, users: List[Dict[str, str]]):
        """
        Inserts users one by one, opening connection for each.
        Should use batch operations and connection reuse.
        """
        user_ids = []
        
        for user in users:
            # Opens new connection for each insert - very inefficient
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    "INSERT INTO users (name, email) VALUES (?, ?)",
                    (user['name'], user['email'])
                )
                user_id = cursor.lastrowid
                await db.commit()
                user_ids.append(user_id)
                
                # Simulates some processing delay
                time.sleep(0.01)  # Should use asyncio.sleep()
        
        return user_ids
    
    async def get_user_posts_inefficiently(self, user_ids: List[int]):
        """
        Fetches posts for users using N+1 query pattern.
        Should use JOIN or IN clause for efficiency.
        """
        results = {}
        
        for user_id in user_ids:
            # N+1 query problem - separate query for each user
            async with aiosqlite.connect(self.db_path) as db:
                # First get user info
                async with db.execute(
                    "SELECT name, email FROM users WHERE id = ?", 
                    (user_id,)
                ) as cursor:
                    user_row = await cursor.fetchone()
                
                if user_row:
                    # Then get posts in separate query
                    async with db.execute(
                        "SELECT title, content FROM posts WHERE user_id = ?",
                        (user_id,)
                    ) as cursor:
                        posts = await cursor.fetchall()
                    
                    results[user_id] = {
                        'user': user_row,
                        'posts': posts
                    }
        
        return results
    
    async def update_posts_without_transactions(self, updates: List[Dict]):
        """
        Updates posts without proper transaction handling.
        Could lead to partial updates on failure.
        """
        success_count = 0
        
        for update in updates:
            try:
                # Each update in separate connection - no transaction safety
                async with aiosqlite.connect(self.db_path) as db:
                    await db.execute(
                        "UPDATE posts SET title = ?, content = ? WHERE id = ?",
                        (update['title'], update['content'], update['id'])
                    )
                    await db.commit()
                    success_count += 1
                    
                    # Simulate processing time
                    await asyncio.sleep(0.05)
                    
            except Exception as e:
                print(f"Failed to update post {update['id']}: {e}")
        
        return success_count
    
    async def search_posts_inefficiently(self, search_terms: List[str]):
        """
        Searches posts with multiple separate queries instead of optimized search.
        Should use full-text search or optimized LIKE queries.
        """
        all_results = []
        
        for term in search_terms:
            # Separate query for each search term
            async with aiosqlite.connect(self.db_path) as db:
                # Inefficient LIKE query without indexes
                async with db.execute(
                    "SELECT id, title, content FROM posts WHERE title LIKE ? OR content LIKE ?",
                    (f"%{term}%", f"%{term}%")
                ) as cursor:
                    results = await cursor.fetchall()
                    
                    # Process results synchronously
                    for row in results:
                        # Simulate some processing
                        processed_row = {
                            'id': row[0],
                            'title': row[1],
                            'content': row[2][:100] + '...' if len(row[2]) > 100 else row[2],
                            'search_term': term
                        }
                        all_results.append(processed_row)
        
        return all_results


async def connection_pool_misuse():
    """
    Demonstrates improper connection handling patterns.
    Should use proper connection pooling.
    """
    db_path = "test_misuse.db"
    
    # Creates many concurrent connections without pooling
    async def worker(worker_id: int):
        for i in range(5):
            # Each worker creates its own connection for each operation
            async with aiosqlite.connect(db_path) as db:
                await db.execute(
                    "INSERT OR REPLACE INTO temp_data (id, data) VALUES (?, ?)",
                    (worker_id * 10 + i, f"Worker {worker_id} data {i}")
                )
                await db.commit()
                
                # Blocking sleep in async context
                time.sleep(0.1)
    
    # Setup table
    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS temp_data (
                id INTEGER PRIMARY KEY,
                data TEXT
            )
        ''')
        await db.commit()
    
    # Run many workers concurrently - overwhelms database
    workers = [worker(i) for i in range(20)]
    await asyncio.gather(*workers)


async def inefficient_bulk_operations():
    """
    Performs bulk database operations inefficiently.
    Should use batch operations and prepared statements.
    """
    db_path = "test_bulk.db"
    
    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS bulk_test (
                id INTEGER PRIMARY KEY,
                value TEXT,
                timestamp REAL
            )
        ''')
        await db.commit()
    
    # Insert 1000 records one by one
    records = [(i, f"value_{i}", time.time()) for i in range(1000)]
    
    for record_id, value, timestamp in records:
        # Individual insert instead of executemany
        async with aiosqlite.connect(db_path) as db:
            await db.execute(
                "INSERT INTO bulk_test (id, value, timestamp) VALUES (?, ?, ?)",
                (record_id, value, timestamp)
            )
            await db.commit()  # Commit each insert individually


async def blocking_database_operations():
    """
    Mixes blocking operations with async database calls.
    Should keep all operations async or use proper thread isolation.
    """
    db_path = "test_blocking.db"
    
    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS blocking_test (
                id INTEGER PRIMARY KEY,
                data TEXT
            )
        ''')
        await db.commit()
    
    for i in range(10):
        # Async database operation
        async with aiosqlite.connect(db_path) as db:
            await db.execute(
                "INSERT INTO blocking_test (data) VALUES (?)",
                (f"async_data_{i}",)
            )
            await db.commit()
        
        # Blocking operation that freezes event loop
        time.sleep(0.5)  # Should use asyncio.sleep()
        
        # CPU-intensive blocking operation
        result = sum(x**2 for x in range(10000))  # Should use asyncio.to_thread()
        
        # More async database work
        async with aiosqlite.connect(db_path) as db:
            await db.execute(
                "UPDATE blocking_test SET data = ? WHERE id = ?",
                (f"updated_data_{result % 1000}", i + 1)
            )
            await db.commit()


if __name__ == "__main__":
    async def main():
        print("Running inefficient database examples...")
        
        # Example 1: Inefficient database manager
        db_manager = InefficientDatabaseManager("test_inefficient.db")
        await db_manager.setup_database()
        
        users = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Bob", "email": "bob@example.com"},
            {"name": "Charlie", "email": "charlie@example.com"}
        ]
        
        start_time = time.time()
        user_ids = await db_manager.insert_users_sequentially(users)
        print(f"Sequential inserts took: {time.time() - start_time:.2f}s")
        
        # Example 2: Connection pool misuse
        start_time = time.time()
        await connection_pool_misuse()
        print(f"Connection misuse took: {time.time() - start_time:.2f}s")
        
        # Example 3: Bulk operations
        start_time = time.time()
        await inefficient_bulk_operations()
        print(f"Inefficient bulk operations took: {time.time() - start_time:.2f}s")
    
    asyncio.run(main())