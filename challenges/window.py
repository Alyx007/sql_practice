challenges = [
    {
        "title": "Rank employees by salary within department",
        "difficulty": "medium",
        "description": (
            "For each employee (who has a valid department), show:\n"
            "name, department name, salary, and their salary rank within\n"
            "that department (highest salary = rank 1).\n"
            "Order by department name, then rank."
        ),
        "expected_sql": """
SELECT e.name, d.name AS department, e.salary,
       ROW_NUMBER() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS salary_rank
FROM employees e
JOIN departments d ON e.dept_id = d.id
ORDER BY d.name, salary_rank;""",
        "hints": [
            "Window functions let you rank without collapsing rows (unlike GROUP BY).",
            "ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) ranks within each dept.",
            "PARTITION BY = reset numbering per group. ORDER BY = what determines the rank.",
        ],
    },
    {
        "title": "Running total of salaries",
        "difficulty": "medium",
        "description": (
            "List all employees ordered by salary (highest first).\n"
            "Show name, salary, running_total (cumulative sum of salaries),\n"
            "and cumulative_pct (running total as % of all salaries, rounded to 1 decimal)."
        ),
        "expected_sql": """
SELECT e.name, e.salary,
       SUM(e.salary) OVER (ORDER BY e.salary DESC) AS running_total,
       ROUND(SUM(e.salary) OVER (ORDER BY e.salary DESC) * 100.0
             / (SELECT SUM(salary) FROM employees), 1) AS cumulative_pct
FROM employees e
ORDER BY e.salary DESC;""",
        "hints": [
            "SUM() can be used as a window function with OVER(ORDER BY ...) for running totals.",
            "SUM(salary) OVER (ORDER BY salary DESC) accumulates as you go down the rows.",
            "For percentage: divide the running total by the total sum (subquery) and multiply by 100.",
        ],
    },
    {
        "title": "Month-over-month revenue",
        "difficulty": "hard",
        "description": (
            "Calculate monthly revenue (from completed orders only) and show:\n"
            "month, revenue, previous month's revenue (prev_month),\n"
            "and the change (revenue minus prev_month).\n"
            "Order by month."
        ),
        "expected_sql": """
WITH monthly AS (
    SELECT strftime('%Y-%m', o.order_date) AS month,
           ROUND(SUM(oi.quantity * p.price), 2) AS revenue
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    WHERE o.status = 'completed'
    GROUP BY strftime('%Y-%m', o.order_date)
)
SELECT month, revenue,
       LAG(revenue) OVER (ORDER BY month) AS prev_month,
       ROUND(revenue - LAG(revenue) OVER (ORDER BY month), 2) AS change
FROM monthly
ORDER BY month;""",
        "hints": [
            "First, calculate monthly revenue with a CTE (GROUP BY month).",
            "Then use LAG(revenue) OVER (ORDER BY month) to access the previous row's value.",
            "In SQLite, use strftime('%Y-%m', order_date) to extract year-month.",
        ],
    },
]
