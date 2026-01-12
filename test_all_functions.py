"""Test script to check if codeflash can optimize each function in the repo."""

import ast
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
            server_config TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            file_path TEXT NOT NULL,
            function_name TEXT NOT NULL,
            server TEXT NOT NULL,
            attempt INTEGER NOT NULL,
            success INTEGER NOT NULL,
            duration_seconds REAL NOT NULL,
            output TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (run_id) REFERENCES runs(id)
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_results_run_id ON results(run_id)")
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_results_function ON results(file_path, function_name)"
    )
    conn.commit()
    return conn


def get_functions_from_file(filepath: Path) -> list[str]:
    """Extract all function names from a Python file."""
    try:
        with open(filepath) as f:
            tree = ast.parse(f.read())
    except SyntaxError:
        return []

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not node.name.startswith("_"):
                functions.append(node.name)
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
    output_lines = []

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd="/Users/krrt7/Desktop/work/optimize-me",
        )

        if process.stdout:
            for line in process.stdout:
                console.print(f"    [dim]{line.rstrip()}[/dim]")
                output_lines.append(line)

        process.wait(timeout=300)
        success = process.returncode == 0
        output = "".join(output_lines)
    except subprocess.TimeoutExpired:
        process.kill()
        success = False
        output = "TIMEOUT after 5 minutes"
    except Exception as e:
        success = False
        output = str(e)

    duration = (datetime.now() - start_time).total_seconds()

    return {
        "file": file_path,
        "function": function,
        "server": server,
        "success": success,
        "duration": duration,
        "output": output[-5000:] if len(output) > 5000 else output,
    }


def save_result(conn: sqlite3.Connection, run_id: str, result: dict, attempt: int):
    """Save a single result to the database."""
    conn.execute(
        """
        INSERT INTO results (run_id, file_path, function_name, server, attempt,
                            success, duration_seconds, output, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            run_id,
            result["file"],
            result["function"],
            result["server"],
            attempt,
            1 if result["success"] else 0,
            result["duration"],
            result["output"],
            datetime.now().isoformat(),
        ),
    )
    conn.commit()


def print_summary(conn: sqlite3.Connection, run_id: str):
    """Print a summary table of results."""
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

    # Show failed functions
    for server in ["prod", "local"]:
        cursor = conn.execute(
            """
            SELECT DISTINCT file_path, function_name
            FROM results WHERE run_id = ? AND server = ? AND success = 0
        """,
            (run_id, server),
        )
        failed = cursor.fetchall()
        if failed:
            console.print(f"\n[red]Functions that failed on {server.upper()}:[/red]")
            for file_path, func_name in failed:
                console.print(f"  [dim]•[/dim] {file_path}::[bold]{func_name}[/bold]")


def main():
    conn = init_db()
    run_id = str(uuid.uuid4())
    src_dir = Path("/Users/krrt7/Desktop/work/optimize-me/src")

    # Collect all functions
    all_functions = []
    for py_file in src_dir.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
        rel_path = str(py_file.relative_to(src_dir.parent))
        functions = get_functions_from_file(py_file)
        for func in functions:
            all_functions.append((rel_path, func))

    # Create run record
    conn.execute(
        """
        INSERT INTO runs (id, started_at, total_functions, server_config)
        VALUES (?, ?, ?, ?)
    """,
        (run_id, datetime.now().isoformat(), len(all_functions), "prod:2,local:2"),
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

    # Server config: 2 prod runs, then 2 local runs
    server_attempts = [("prod", 1), ("prod", 2), ("local", 1), ("local", 2)]
    total_tests = len(all_functions) * len(server_attempts)
    completed = 0
    successes = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("({task.completed}/{task.total})"),
        console=console,
    ) as progress:
        overall_task = progress.add_task(
            "[bold blue]Overall Progress", total=total_tests
        )

        for server_idx, (server, attempt) in enumerate(server_attempts):
            server_color = "green" if server == "prod" else "yellow"
            console.print(
                f"\n[bold {server_color}]═══ RUN {server_idx + 1}/4: "
                f"Server={server.upper()}, Attempt={attempt} ═══[/bold {server_color}]"
            )

            for i, (file_path, func_name) in enumerate(all_functions):
                console.print(
                    f"\n[cyan][{i + 1}/{len(all_functions)}][/cyan] "
                    f"[bold]{file_path}[/bold]::[magenta]{func_name}[/magenta]"
                )

                result = run_codeflash(file_path, func_name, server)
                save_result(conn, run_id, result, attempt)

                completed += 1
                if result["success"]:
                    successes += 1
                    console.print(
                        f"  [green]✓ SUCCESS[/green] ({result['duration']:.1f}s)"
                    )
                else:
                    console.print(
                        f"  [red]✗ FAILED[/red] ({result['duration']:.1f}s)"
                    )

                progress.update(overall_task, completed=completed)

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
            f"Results saved to: [cyan]{DB_PATH}[/cyan]\n" f"Run ID: [bold]{run_id}[/bold]",
            title="[green]Test Complete[/green]",
        )
    )

    conn.close()


if __name__ == "__main__":
    main()
