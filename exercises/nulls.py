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
""",
    "questions": [
        {
            "question": "What does `SELECT NULL = NULL` return?",
            "options": ["A) TRUE", "B) FALSE", "C) NULL", "D) An error"],
            "answer": "C",
            "explanation": "In SQL, any comparison with NULL returns NULL (not TRUE or FALSE). That's why you must use IS NULL / IS NOT NULL instead of = NULL.",
        },
        {
            "question": "What does COALESCE(NULL, NULL, 'fallback', 'ignored') return?",
            "options": ["A) NULL", "B) 'fallback'", "C) 'ignored'", "D) An error"],
            "answer": "B",
            "explanation": "COALESCE returns the first non-NULL argument. It skips the two NULLs and returns 'fallback'. It never reaches 'ignored'.",
        },
        {
            "question": "How do you find customers who have NEVER placed an order?",
            "options": ["A) SELECT * FROM customers WHERE orders IS NULL", "B) SELECT * FROM customers c LEFT JOIN orders o ON c.id = o.customer_id WHERE o.id IS NULL", "C) SELECT * FROM customers c INNER JOIN orders o ON c.id = o.customer_id WHERE o.id IS NULL", "D) SELECT * FROM customers WHERE id NOT IN (orders)"],
            "answer": "B",
            "explanation": "The anti-join pattern: LEFT JOIN keeps all customers, then WHERE o.id IS NULL filters to only those with no matching order. INNER JOIN would drop them.",
        },
    ],
}
