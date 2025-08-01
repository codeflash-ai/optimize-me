"""
Inefficient async file I/O operations.
These examples use poor async patterns that defeat the purpose of async programming.
"""

import asyncio
import aiofiles
import time
from pathlib import Path


async def read_files_sequentially(file_paths):
    """
    Reads files one by one, completely defeating the purpose of async.
    Should use asyncio.gather() or similar for concurrent reading.
    """
    results = []
    for file_path in file_paths:
        try:
            async with aiofiles.open(file_path, 'r') as f:
                content = await f.read()
                results.append(content)
        except FileNotFoundError:
            results.append("")
    return results


async def write_files_with_blocking_operations(data_list, base_path):
    """
    Mixes blocking and non-blocking operations inefficiently.
    Uses time.sleep() instead of asyncio.sleep() and processes files sequentially.
    """
    results = []
    for i, data in enumerate(data_list):
        # Blocking sleep - should use asyncio.sleep()
        time.sleep(0.1)  
        
        file_path = Path(base_path) / f"file_{i}.txt"
        # Creates directory synchronously - should use async version
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(file_path, 'w') as f:
            await f.write(str(data))
        
        results.append(file_path)
    
    return results


async def process_large_file_inefficiently(file_path):
    """
    Reads entire large file into memory at once instead of streaming.
    Should process in chunks for better memory efficiency.
    """
    async with aiofiles.open(file_path, 'r') as f:
        # Reads entire file at once - memory inefficient
        content = await f.read()
    
    # Process line by line after loading everything
    lines = content.split('\n')
    processed_lines = []
    
    for line in lines:
        # Simulate some processing with blocking sleep
        time.sleep(0.001)
        processed_lines.append(line.upper())
    
    return processed_lines


async def copy_files_sequentially(source_paths, dest_dir):
    """
    Copies files one by one instead of concurrently.
    Also uses inefficient read-all-then-write-all approach.
    """
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    copied_files = []
    for source_path in source_paths:
        source_path = Path(source_path)
        dest_path = dest_dir / source_path.name
        
        # Read entire file into memory
        async with aiofiles.open(source_path, 'rb') as src:
            data = await src.read()
        
        # Write entire file from memory
        async with aiofiles.open(dest_path, 'wb') as dst:
            await dst.write(data)
        
        copied_files.append(dest_path)
    
    return copied_files


async def monitor_files_inefficiently(file_paths, check_interval=1.0):
    """
    Monitors file changes by repeatedly checking all files sequentially.
    Should use concurrent checking and file system events.
    """
    last_modified = {}
    
    while True:
        changes = []
        
        # Check each file sequentially
        for file_path in file_paths:
            try:
                # Blocking file stat - should use aiofiles.os.stat
                stat_result = Path(file_path).stat()
                current_mtime = stat_result.st_mtime
                
                if file_path not in last_modified:
                    last_modified[file_path] = current_mtime
                elif last_modified[file_path] != current_mtime:
                    changes.append(file_path)
                    last_modified[file_path] = current_mtime
                    
            except FileNotFoundError:
                if file_path in last_modified:
                    changes.append(f"{file_path} (deleted)")
                    del last_modified[file_path]
        
        if changes:
            print(f"File changes detected: {changes}")
        
        # Blocking sleep instead of asyncio.sleep
        time.sleep(check_interval)


if __name__ == "__main__":
    # Example usage
    async def main():
        # Create some test files
        test_files = ["test1.txt", "test2.txt", "test3.txt"]
        test_data = ["Hello World", "Async Programming", "Code Optimization"]
        
        await write_files_with_blocking_operations(test_data, "temp_files")
        
        file_paths = [f"temp_files/file_{i}.txt" for i in range(len(test_data))]
        contents = await read_files_sequentially(file_paths)
        
        print("File contents:", contents)
    
    asyncio.run(main())