exercise = {
    "title": "GROUP BY + HAVING + aggregate functions",
    "description": "Find departments with total salary > 150k, showing count and average.",
    "queries": {
        "Aggregation with HAVING": """
SELECT d.name AS department,
       COUNT(e.id) AS employee_count,
       ROUND(SUM(e.salary), 0) AS total_salary,
       ROUND(AVG(e.salary), 0) AS avg_salary,
       MIN(e.salary) AS min_salary,
       MAX(e.salary) AS max_salary
FROM employees e
JOIN departments d ON e.dept_id = d.id
GROUP BY d.name
HAVING SUM(e.salary) > 150000
ORDER BY total_salary DESC;""",
    },
    "explanation": """
WHERE filters rows BEFORE grouping. HAVING filters groups AFTER aggregation.
You can't write WHERE SUM(salary) > X — that's invalid.
Use WHERE for row-level filters, HAVING for group-level filters.

Execution order: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
"""
}
