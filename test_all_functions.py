"""Test script to check if codeflash can optimize each function in the repo."""

import ast
import re
import sqlite3
import subprocess
import uuid
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()
DB_PATH = Path("/Users/krrt7/Desktop/work/optimize-me/codeflash_results.db")


def init_db() -> sqlite3.Connection:
    """Initialize the SQLite database with schema."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id TEXT PRIMARY KEY,
            started_at TEXT NOT NULL,
            completed_at TEXT,
            total_functions INTEGER,
            server_config TEXT,
            codeflash_version TEXT,
            python_version TEXT,
            git_commit TEXT,
            git_branch TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            file_path TEXT NOT NULL,
            function_name TEXT NOT NULL,
            function_line_start INTEGER,
            function_line_count INTEGER,
            server TEXT NOT NULL,
            attempt INTEGER NOT NULL,
            success INTEGER NOT NULL,
            exit_code INTEGER,
            error_type TEXT,
            duration_seconds REAL NOT NULL,
            stdout TEXT,
            stderr TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (run_id) REFERENCES runs(id)
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_results_run_id ON results(run_id)")
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_results_function ON results(file_path, function_name)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_results_error_type ON results(error_type)"
    )
    conn.commit()
    return conn


def get_environment_info() -> dict:
    """Get environment information for debugging."""
    info = {}

    # Codeflash version
    try:
        result = subprocess.run(
            ["uv", "run", "codeflash", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd="/Users/krrt7/Desktop/work/optimize-me",
        )
        info["codeflash_version"] = result.stdout.strip() or result.stderr.strip()
    except Exception:
        info["codeflash_version"] = "unknown"

    # Python version
    try:
        result = subprocess.run(
            ["uv", "run", "python", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd="/Users/krrt7/Desktop/work/optimize-me",
        )
        info["python_version"] = result.stdout.strip()
    except Exception:
        info["python_version"] = "unknown"

    # Git commit
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd="/Users/krrt7/Desktop/work/optimize-me",
        )
        info["git_commit"] = result.stdout.strip()[:12]
    except Exception:
        info["git_commit"] = "unknown"

    # Git branch
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd="/Users/krrt7/Desktop/work/optimize-me",
        )
        info["git_branch"] = result.stdout.strip()
    except Exception:
        info["git_branch"] = "unknown"

    return info


def classify_error(stdout: str, stderr: str, exit_code: int | None) -> str:
    """Classify the error type from output."""
    combined = stdout + stderr

    if exit_code == 0:
        return "success"

    if "TIMEOUT" in combined:
        return "timeout"

    # Check for common error patterns
    error_patterns = [
        (r"No tests found", "no_tests_found"),
        (r"Test.*failed", "test_failure"),
        (r"SyntaxError", "syntax_error"),
        (r"ImportError|ModuleNotFoundError", "import_error"),
        (r"TypeError", "type_error"),
        (r"ValueError", "value_error"),
        (r"AttributeError", "attribute_error"),
        (r"KeyError", "key_error"),
        (r"IndexError", "index_error"),
        (r"RuntimeError", "runtime_error"),
        (r"MemoryError", "memory_error"),
        (r"RecursionError", "recursion_error"),
        (r"ConnectionError|ConnectionRefused|HTTPError", "connection_error"),
        (r"API.*error|rate.?limit", "api_error"),
        (r"No optimization found|could not find.*optimization", "no_optimization"),
        (r"Traceback", "exception"),
    ]

    for pattern, error_type in error_patterns:
        if re.search(pattern, combined, re.IGNORECASE):
            return error_type

    return "unknown_error"


def get_function_info(filepath: Path) -> list[dict]:
    """Extract function names with metadata from a Python file."""
    try:
        with open(filepath) as f:
            source = f.read()
            tree = ast.parse(source)
    except SyntaxError:
        return []

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not node.name.startswith("_"):
                # Calculate line count
                end_line = node.end_lineno or node.lineno
                line_count = end_line - node.lineno + 1
                functions.append(
                    {
                        "name": node.name,
                        "line_start": node.lineno,
                        "line_count": line_count,
                    }
                )
    return functions


def run_codeflash(file_path: str, function: str, server: str) -> dict:
    """Run codeflash on a specific function and return the result with live output."""
    cmd = [
        "uv",
        "run",
        "codeflash",
        "--file",
        file_path,
        "--function",
        function,
        "--server",
        server,
        "--no-pr",
    ]

    start_time = datetime.now()
    stdout_lines = []
    stderr_lines = []
    exit_code = None

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            cwd="/Users/krrt7/Desktop/work/optimize-me",
        )

        # Read stdout in real-time
        if process.stdout:
            for line in process.stdout:
                console.print(f"    [dim]{line.rstrip()}[/dim]")
                stdout_lines.append(line)

        # Read any remaining stderr
        if process.stderr:
            stderr_lines = process.stderr.readlines()
            for line in stderr_lines:
                if line.strip():
                    console.print(f"    [red dim]{line.rstrip()}[/red dim]")

        process.wait(timeout=300)
        exit_code = process.returncode
        success = exit_code == 0
        stdout = "".join(stdout_lines)
        stderr = "".join(stderr_lines)
    except subprocess.TimeoutExpired:
        process.kill()
        exit_code = -1
        success = False
        stdout = "".join(stdout_lines)
        stderr = "TIMEOUT after 5 minutes"
    except Exception as e:
        exit_code = -2
        success = False
        stdout = "".join(stdout_lines)
        stderr = str(e)

    duration = (datetime.now() - start_time).total_seconds()
    error_type = classify_error(stdout, stderr, exit_code)

    return {
        "file": file_path,
        "function": function,
        "server": server,
        "success": success,
        "exit_code": exit_code,
        "error_type": error_type,
        "duration": duration,
        "stdout": stdout,
        "stderr": stderr,
    }


def save_result(
    conn: sqlite3.Connection,
    run_id: str,
    result: dict,
    attempt: int,
    func_info: dict,
):
    """Save a single result to the database."""
    conn.execute(
        """
        INSERT INTO results (run_id, file_path, function_name, function_line_start,
                            function_line_count, server, attempt, success, exit_code,
                            error_type, duration_seconds, stdout, stderr, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            run_id,
            result["file"],
            result["function"],
            func_info.get("line_start"),
            func_info.get("line_count"),
            result["server"],
            attempt,
            1 if result["success"] else 0,
            result["exit_code"],
            result["error_type"],
            result["duration"],
            result["stdout"],
            result["stderr"],
            datetime.now().isoformat(),
        ),
    )
    conn.commit()


def print_summary(conn: sqlite3.Connection, run_id: str):
    """Print a summary table of results."""
    # Overall results table
    table = Table(title="Test Results Summary")
    table.add_column("Server", style="cyan")
    table.add_column("Success", style="green")
    table.add_column("Failed", style="red")
    table.add_column("Total", style="blue")
    table.add_column("Success Rate", style="yellow")

    for server in ["prod", "local"]:
        cursor = conn.execute(
            """
            SELECT COUNT(*) as total, SUM(success) as successes
            FROM results WHERE run_id = ? AND server = ?
        """,
            (run_id, server),
        )
        row = cursor.fetchone()
        total, successes = row[0], row[1] or 0
        failed = total - successes
        rate = f"{(successes / total * 100):.1f}%" if total > 0 else "N/A"
        table.add_row(server.upper(), str(successes), str(failed), str(total), rate)

    console.print()
    console.print(table)

    # Error type breakdown
    error_table = Table(title="Error Type Breakdown")
    error_table.add_column("Error Type", style="red")
    error_table.add_column("Count", style="yellow")
    error_table.add_column("Percentage", style="cyan")

    cursor = conn.execute(
        """
        SELECT error_type, COUNT(*) as count
        FROM results
        WHERE run_id = ? AND success = 0
        GROUP BY error_type
        ORDER BY count DESC
    """,
        (run_id,),
    )
    error_rows = cursor.fetchall()
    total_errors = sum(row[1] for row in error_rows)

    for error_type, count in error_rows:
        pct = f"{(count / total_errors * 100):.1f}%" if total_errors > 0 else "N/A"
        error_table.add_row(error_type, str(count), pct)

    if error_rows:
        console.print()
        console.print(error_table)

    # Flakiness detection (functions that succeeded on one attempt but failed on another)
    cursor = conn.execute(
        """
        SELECT file_path, function_name, server,
               SUM(success) as successes, COUNT(*) as attempts
        FROM results
        WHERE run_id = ?
        GROUP BY file_path, function_name, server
        HAVING successes > 0 AND successes < attempts
    """,
        (run_id,),
    )
    flaky = cursor.fetchall()
    if flaky:
        console.print("\n[yellow]Flaky functions (inconsistent results):[/yellow]")
        for file_path, func_name, server, successes, attempts in flaky:
            console.print(
                f"  [dim]•[/dim] {file_path}::[bold]{func_name}[/bold] "
                f"({server}): {successes}/{attempts} succeeded"
            )

    # Show failed functions
    for server in ["prod", "local"]:
        cursor = conn.execute(
            """
            SELECT DISTINCT file_path, function_name, error_type
            FROM results WHERE run_id = ? AND server = ? AND success = 0
            ORDER BY error_type, file_path, function_name
        """,
            (run_id, server),
        )
        failed = cursor.fetchall()
        if failed:
            console.print(f"\n[red]Functions that failed on {server.upper()}:[/red]")
            current_error_type = None
            for file_path, func_name, error_type in failed:
                if error_type != current_error_type:
                    console.print(f"  [{error_type}]")
                    current_error_type = error_type
                console.print(f"    [dim]•[/dim] {file_path}::[bold]{func_name}[/bold]")


def main():
    conn = init_db()
    run_id = str(uuid.uuid4())
    src_dir = Path("/Users/krrt7/Desktop/work/optimize-me/src")

    # Get environment info
    env_info = get_environment_info()
    console.print(f"[dim]Codeflash: {env_info['codeflash_version']}[/dim]")
    console.print(f"[dim]Python: {env_info['python_version']}[/dim]")
    console.print(f"[dim]Git: {env_info['git_branch']}@{env_info['git_commit']}[/dim]")

    # Collect all functions with metadata
    all_functions = []
    for py_file in src_dir.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
        rel_path = str(py_file.relative_to(src_dir.parent))
        func_infos = get_function_info(py_file)
        for func_info in func_infos:
            all_functions.append((rel_path, func_info))

    # Create run record
    conn.execute(
        """
        INSERT INTO runs (id, started_at, total_functions, server_config,
                         codeflash_version, python_version, git_commit, git_branch)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            run_id,
            datetime.now().isoformat(),
            len(all_functions),
            "prod:2,local:2(fallback)",
            env_info["codeflash_version"],
            env_info["python_version"],
            env_info["git_commit"],
            env_info["git_branch"],
        ),
    )
    conn.commit()

    # Header
    console.print(
        Panel.fit(
            f"[bold]Codeflash Optimization Test[/bold]\n"
            f"Run ID: [cyan]{run_id}[/cyan]\n"
            f"Database: [dim]{DB_PATH}[/dim]\n"
            f"Functions: [green]{len(all_functions)}[/green]",
            title="Starting Test",
        )
    )

    # Track results per function
    # Key: (file_path, func_name), Value: {"prod": [bool, bool], "local": [bool, bool]}
    func_results: dict[tuple[str, str], dict[str, list[bool]]] = {}

    def run_functions_on_server(
        functions: list[tuple[str, dict]],
        server: str,
        attempts: list[int],
        progress,
        task_id,
        completed_ref: list[int],
    ):
        """Run a list of functions on a specific server for given attempts."""
        for attempt in attempts:
            server_color = "green" if server == "prod" else "yellow"
            console.print(
                f"\n[bold {server_color}]═══ Server={server.upper()}, "
                f"Attempt={attempt} ═══[/bold {server_color}]"
            )

            for i, (file_path, func_info) in enumerate(functions):
                func_name = func_info["name"]
                func_key = (file_path, func_name)

                console.print(
                    f"\n[cyan][{i + 1}/{len(functions)}][/cyan] "
                    f"[bold]{file_path}[/bold]::[magenta]{func_name}[/magenta] "
                    f"[dim](L{func_info['line_start']}, {func_info['line_count']} lines)[/dim]"
                )

                result = run_codeflash(file_path, func_name, server)
                save_result(conn, run_id, result, attempt, func_info)

                # Track result
                if func_key not in func_results:
                    func_results[func_key] = {"prod": [], "local": []}
                func_results[func_key][server].append(result["success"])

                completed_ref[0] += 1
                if result["success"]:
                    console.print(
                        f"  [green]✓ SUCCESS[/green] ({result['duration']:.1f}s)"
                    )
                else:
                    console.print(
                        f"  [red]✗ FAILED[/red] [{result['error_type']}] ({result['duration']:.1f}s)"
                    )

                progress.update(task_id, completed=completed_ref[0])

    # Phase 1: Run all functions on prod (2 attempts)
    # Phase 2: Run failed functions on local (2 attempts)
    # Estimate total: all functions * 2 (prod) + some fraction for local
    # We'll update the total dynamically after prod phase

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("({task.completed}/{task.total})"),
        console=console,
    ) as progress:
        # Start with prod estimate
        prod_total = len(all_functions) * 2
        overall_task = progress.add_task(
            "[bold blue]Overall Progress", total=prod_total
        )
        completed = [0]  # Use list for mutability in nested function

        # Phase 1: PROD server (2 attempts for all functions)
        console.print(
            "\n[bold cyan]══════════════════════════════════════════════════════════[/bold cyan]"
        )
        console.print("[bold cyan]PHASE 1: Testing all functions on PROD server[/bold cyan]")
        console.print(
            "[bold cyan]══════════════════════════════════════════════════════════[/bold cyan]"
        )

        run_functions_on_server(
            all_functions, "prod", [1, 2], progress, overall_task, completed
        )

        # Determine which functions failed on prod (both attempts failed)
        failed_on_prod = []
        for file_path, func_info in all_functions:
            func_key = (file_path, func_info["name"])
            prod_results = func_results.get(func_key, {}).get("prod", [])
            # If no success in any prod attempt, try local
            if not any(prod_results):
                failed_on_prod.append((file_path, func_info))

        console.print(
            f"\n[yellow]Functions that failed on PROD: {len(failed_on_prod)}/{len(all_functions)}[/yellow]"
        )

        # Phase 2: LOCAL server (only for functions that failed on prod)
        if failed_on_prod:
            console.print(
                "\n[bold yellow]══════════════════════════════════════════════════════════[/bold yellow]"
            )
            console.print(
                f"[bold yellow]PHASE 2: Testing {len(failed_on_prod)} failed functions on LOCAL server[/bold yellow]"
            )
            console.print(
                "[bold yellow]══════════════════════════════════════════════════════════[/bold yellow]"
            )

            # Update progress total to include local attempts
            local_total = len(failed_on_prod) * 2
            new_total = prod_total + local_total
            progress.update(overall_task, total=new_total)

            run_functions_on_server(
                failed_on_prod, "local", [1, 2], progress, overall_task, completed
            )
        else:
            console.print(
                "\n[green]All functions succeeded on PROD - skipping LOCAL phase[/green]"
            )

    # Update run as completed
    conn.execute(
        "UPDATE runs SET completed_at = ? WHERE id = ?",
        (datetime.now().isoformat(), run_id),
    )
    conn.commit()

    # Print summary
    console.print("\n")
    print_summary(conn, run_id)

    console.print(
        Panel.fit(
            f"Results saved to: [cyan]{DB_PATH}[/cyan]\nRun ID: [bold]{run_id}[/bold]",
            title="[green]Test Complete[/green]",
        )
    )

    conn.close()


if __name__ == "__main__":
    main()
