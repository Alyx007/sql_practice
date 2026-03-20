"""Database connection and query runner."""

import sqlite3
from tabulate import tabulate


def connect(db_path="sql_practice/practice.db"):
    return sqlite3.connect(db_path)


def run_query(conn, sql):
    """Execute SQL and print results as a formatted table."""
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        if not rows:
            print("\n(empty result)\n")
            return
        headers = [desc[0] for desc in cur.description]
        print("\n" + tabulate(rows, headers=headers, tablefmt="psql") + "\n")
        print(f"({len(rows)} rows)")
    except Exception as e:
        print(f"\nSQL Error: {e}\n")


def fetch_query(conn, sql):
    """Execute SQL and return (headers, rows) or (None, error_string)."""
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        headers = [desc[0] for desc in cur.description] if cur.description else []
        return headers, rows
    except Exception as e:
        return None, str(e)


def print_result(headers, rows):
    """Print a (headers, rows) result as a formatted table."""
    if not rows:
        print("\n(empty result)\n")
        return
    print("\n" + tabulate(rows, headers=headers, tablefmt="psql") + "\n")
    print(f"({len(rows)} rows)")


def results_match(conn, user_sql, expected_sql):
    """Compare user's query result against expected. Returns (match, user_res, expected_res, error)."""
    user_res = fetch_query(conn, user_sql)
    if user_res[0] is None:
        return False, None, None, user_res[1]

    expected_res = fetch_query(conn, expected_sql)

    user_headers, user_rows = user_res
    exp_headers, exp_rows = expected_res

    # Compare sorted rows (order-insensitive)
    match = sorted(user_rows) == sorted(exp_rows)
    return match, user_res, expected_res, None


def read_sql_input(prompt="SQL> "):
    """Read multi-line SQL input until ; or a single-word command."""
    lines = []
    current_prompt = prompt
    while True:
        line = input(current_prompt)
        stripped = line.strip().lower()
        if not lines and stripped in ("hint", "skip", "solution", "quit", "q", "tables", "help"):
            return stripped
        lines.append(line)
        if line.strip().endswith(";"):
            return " ".join(lines)
        current_prompt = "...> "
