"""Load seed data and display table info."""

import os


def load_seed(conn):
    """Read and execute seed.sql to populate the database."""
    seed_path = os.path.join(os.path.dirname(__file__), "seed.sql")
    with open(seed_path) as f:
        conn.executescript(f.read())
    conn.commit()


def show_tables():
    """Print available tables, their columns, and relationships."""
    tables = {
        "departments": "id, name, budget                                    (6 rows)",
        "employees":   "id, name, dept_id, salary, hire_date, manager_id    (15 rows)",
        "customers":   "id, name, city, segment                             (10 rows)",
        "products":    "id, name, category, price                           (8 rows)",
        "orders":      "id, customer_id, order_date, status                 (20 rows)",
        "order_items": "id, order_id, product_id, quantity                  (24 rows)",
    }

    print("\n--- Tables ---\n")
    for name, cols in tables.items():
        print(f"  {name:15s}  {cols}")

    print("\n--- Relationships ---\n")
    print("  employees.dept_id     -> departments.id")
    print("  employees.manager_id  -> employees.id")
    print("  orders.customer_id    -> customers.id")
    print("  order_items.order_id  -> orders.id")
    print("  order_items.product_id -> products.id")

    print("\n--- What can you practice here? ---\n")
    print("  The data has built-in edge cases to help you explore different scenarios:\n")
    print("  JOINs:")
    print("    - Karen & Leo have no department (NULL dept_id) — what happens in LEFT vs INNER JOIN?")
    print("    - Mona's dept_id is 99 (doesn't exist) — how do orphaned references behave?")
    print("    - Legal department has no employees — when does it appear, when does it vanish?")
    print("    - Try: compare INNER, LEFT, and RIGHT JOIN on employees + departments\n")
    print("  Aggregations:")
    print("    - Group employees by department — which dept has the highest avg salary?")
    print("    - Count orders per customer — who are the most active buyers?")
    print("    - Calculate total revenue per product (order_items x products)\n")
    print("  Window functions:")
    print("    - Rank employees by salary within each department (ROW_NUMBER, RANK)")
    print("    - Running total of order amounts over time")
    print("    - Compare each month's revenue to the previous month (LAG)\n")
    print("  NULLs & data quality:")
    print("    - Kappa Digital (customer 10) has never placed an order — can you find them?")
    print("    - Some employees have no manager (NULL manager_id) — use COALESCE for clean output")
    print("    - Find all 'orphaned' data: employees without valid depts, orders without items\n")
    print("  Multi-step analysis (CTEs):")
    print("    - Chain queries: orders -> revenue per order -> revenue per customer -> top 5")
    print("    - Calculate month-over-month growth with percentage change")
    print("    - Build a pivot table: order counts by status per customer (CASE WHEN)\n")
