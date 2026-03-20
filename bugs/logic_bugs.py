bugs = [
    {
        "title": "NULL comparison trap",
        "description": (
            "This query should find employees who have no department assigned.\n"
            "But it returns 0 rows even though Karen and Leo have NULL dept_id!"
        ),
        "buggy_sql": """
SELECT name, dept_id
FROM employees
WHERE dept_id = NULL;""",
        "expected_sql": """
SELECT name, dept_id
FROM employees
WHERE dept_id IS NULL;""",
        "hint": "In SQL, nothing is ever EQUAL to NULL — not even NULL itself. There's a special operator for checking NULLs.",
        "explanation": "NULL represents 'unknown'. The expression NULL = NULL evaluates to NULL (unknown), not TRUE. Always use IS NULL or IS NOT NULL to check for NULLs.",
    },
    {
        "title": "Wrong salary ranking — gaps in ranks",
        "description": (
            "This query ranks employees in Sales department by salary.\n"
            "If two people share a salary, the next rank should follow immediately\n"
            "(e.g., 1, 2, 2, 3 — no gaps). But the current query produces gaps\n"
            "when there are ties (e.g., 1, 2, 2, 4).\n"
            "Note: Frank=82000, Grace=82000 (tie!), Hank=68000, Ivy=68000 (tie!)."
        ),
        "buggy_sql": """
SELECT e.name, e.salary,
       RANK() OVER (ORDER BY e.salary DESC) AS salary_rank
FROM employees e
WHERE e.dept_id = 3
ORDER BY salary_rank;""",
        "expected_sql": """
SELECT e.name, e.salary,
       DENSE_RANK() OVER (ORDER BY e.salary DESC) AS salary_rank
FROM employees e
WHERE e.dept_id = 3
ORDER BY salary_rank;""",
        "hint": "There are 3 ranking functions: ROW_NUMBER (always unique), RANK (gaps after ties), and one more that has no gaps...",
        "explanation": "RANK() skips numbers after ties (1,2,2,4). DENSE_RANK() never skips (1,2,2,3). Use DENSE_RANK() when you want consecutive ranks without gaps.",
    },
    {
        "title": "Incorrect percentage calculation — integer division",
        "description": (
            "This query should show what percentage of total employees each\n"
            "department has. But all percentages show as 0!"
        ),
        "buggy_sql": """
SELECT d.name AS department,
       COUNT(e.id) AS emp_count,
       ROUND(COUNT(e.id) / (SELECT COUNT(*) FROM employees) * 100, 1) AS pct
FROM employees e
JOIN departments d ON e.dept_id = d.id
GROUP BY d.name
ORDER BY pct DESC;""",
        "expected_sql": """
SELECT d.name AS department,
       COUNT(e.id) AS emp_count,
       ROUND(COUNT(e.id) * 100.0 / (SELECT COUNT(*) FROM employees), 1) AS pct
FROM employees e
JOIN departments d ON e.dept_id = d.id
GROUP BY d.name
ORDER BY pct DESC;""",
        "hint": "In SQL, dividing an integer by a larger integer gives 0 (integer division). How do you force decimal division?",
        "explanation": "4 / 15 = 0 in integer division. Multiply by 100.0 (a float) BEFORE dividing to force decimal arithmetic: 4 * 100.0 / 15 = 26.7.",
    },
]
