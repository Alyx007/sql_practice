exercise = {
    "title": "Subqueries and NULL handling",
    "description": "Find missing data and handle NULLs cleanly.",
    "queries": {
        "Customers with no orders (anti-join pattern)": """
SELECT c.name, c.city, c.segment
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;""",

        "COALESCE to replace NULLs": """
SELECT e.name,
       COALESCE(d.name, 'No Department') AS department,
       e.salary,
       COALESCE(m.name, 'No Manager') AS manager
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id
LEFT JOIN employees m ON e.manager_id = m.id
ORDER BY department, e.name;""",
    },
    "explanation": """
Anti-join pattern:  LEFT JOIN + WHERE right.id IS NULL
  = "find rows with NO match". Very useful for data quality checks.

COALESCE(a, b, c) returns the first non-NULL value.
  Useful for fallback defaults in reports and pipelines.

Remember: NULL = NULL is NOT true. Always use IS NULL / IS NOT NULL.
"""
}
