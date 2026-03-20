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
""",
    "questions": [
        {
            "question": "You want to exclude employees with salary < 50000 BEFORE grouping by department. Which clause do you use?",
            "options": ["A) HAVING salary >= 50000", "B) WHERE salary >= 50000", "C) GROUP BY salary >= 50000", "D) LIMIT salary >= 50000"],
            "answer": "B",
            "explanation": "WHERE filters individual rows before GROUP BY runs. HAVING only works on aggregated results after grouping.",
        },
        {
            "question": "What is the correct SQL execution order?",
            "options": ["A) SELECT -> FROM -> WHERE -> GROUP BY -> HAVING", "B) FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY", "C) FROM -> GROUP BY -> WHERE -> HAVING -> SELECT", "D) SELECT -> FROM -> GROUP BY -> WHERE -> HAVING"],
            "answer": "B",
            "explanation": "SQL executes: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT. This is why you can't use column aliases in WHERE but can in ORDER BY.",
        },
        {
            "question": "Which query is INVALID?",
            "options": ["A) SELECT dept_id, AVG(salary) FROM employees GROUP BY dept_id HAVING AVG(salary) > 70000", "B) SELECT dept_id, AVG(salary) FROM employees WHERE AVG(salary) > 70000 GROUP BY dept_id", "C) SELECT dept_id, COUNT(*) FROM employees GROUP BY dept_id", "D) SELECT dept_id, MAX(salary) FROM employees GROUP BY dept_id HAVING COUNT(*) > 2"],
            "answer": "B",
            "explanation": "You cannot use aggregate functions (AVG, SUM, COUNT, etc.) in a WHERE clause. Aggregates require HAVING because they operate on groups, not individual rows.",
        },
    ],
}
