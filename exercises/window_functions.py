exercise = {
    "title": "Window functions: ROW_NUMBER, RANK, running totals",
    "description": "Rank employees by salary within each department + compute running totals.",
    "queries": {
        "ROW_NUMBER (rank within department)": """
SELECT e.name, d.name AS dept, e.salary,
       ROW_NUMBER() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS rank_in_dept
FROM employees e
JOIN departments d ON e.dept_id = d.id
ORDER BY d.name, rank_in_dept;""",

        "Running total of salaries": """
SELECT e.name, e.salary,
       SUM(e.salary) OVER (ORDER BY e.salary DESC) AS running_total,
       ROUND(SUM(e.salary) OVER (ORDER BY e.salary DESC) * 100.0 /
             (SELECT SUM(salary) FROM employees), 1) AS cumulative_pct
FROM employees e
ORDER BY e.salary DESC;""",
    },
    "explanation": """
Window functions compute across rows WITHOUT collapsing them (unlike GROUP BY).
  PARTITION BY = reset the calculation for each group
  ORDER BY inside OVER() = in what order to process rows

ROW_NUMBER: always unique (1,2,3)
RANK:       ties share rank, gaps after (1,1,3)
DENSE_RANK: ties share rank, no gaps   (1,1,2)
"""
}
