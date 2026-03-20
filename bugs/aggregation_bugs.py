bugs = [
    {
        "title": "HAVING vs WHERE mixup",
        "description": (
            "This query should find departments where the average salary is above 75000.\n"
            "But it throws an error!"
        ),
        "buggy_sql": """
SELECT d.name AS department, ROUND(AVG(e.salary), 0) AS avg_salary
FROM employees e
JOIN departments d ON e.dept_id = d.id
WHERE AVG(e.salary) > 75000
GROUP BY d.name
ORDER BY avg_salary DESC;""",
        "expected_sql": """
SELECT d.name AS department, ROUND(AVG(e.salary), 0) AS avg_salary
FROM employees e
JOIN departments d ON e.dept_id = d.id
GROUP BY d.name
HAVING AVG(e.salary) > 75000
ORDER BY avg_salary DESC;""",
        "hint": "You can't use aggregate functions in WHERE. There's another keyword for filtering after GROUP BY.",
        "explanation": "WHERE runs before GROUP BY so it can't see aggregates. Use HAVING after GROUP BY to filter on aggregate results.",
    },
    {
        "title": "COUNT(*) vs COUNT(column) confusion",
        "description": (
            "This query should count how many employees have a manager.\n"
            "But it shows 15 (total employees) instead of the correct count!"
        ),
        "buggy_sql": """
SELECT COUNT(*) AS employees_with_manager
FROM employees;""",
        "expected_sql": """
SELECT COUNT(manager_id) AS employees_with_manager
FROM employees;""",
        "hint": "COUNT(*) counts ALL rows regardless of NULL values. How do you count only non-NULL values in a specific column?",
        "explanation": "COUNT(*) counts every row. COUNT(column) counts only non-NULL values in that column. Since manager_id is NULL for employees without a manager, COUNT(manager_id) gives the correct count.",
    },
    {
        "title": "Missing product in revenue report",
        "description": (
            "This query calculates revenue per product from completed orders.\n"
            "But products that were never ordered should still appear with 0 revenue.\n"
            "Currently, 'CI/CD Pipeline' is missing!"
        ),
        "buggy_sql": """
SELECT p.name AS product,
       COALESCE(ROUND(SUM(oi.quantity * p.price), 2), 0) AS revenue
FROM products p
JOIN order_items oi ON p.id = oi.product_id
JOIN orders o ON oi.order_id = o.id AND o.status = 'completed'
GROUP BY p.name
ORDER BY revenue DESC;""",
        "expected_sql": """
SELECT p.name AS product,
       COALESCE(ROUND(SUM(oi.quantity * p.price), 2), 0) AS revenue
FROM products p
LEFT JOIN order_items oi ON p.id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.id AND o.status = 'completed'
GROUP BY p.name
ORDER BY revenue DESC;""",
        "hint": "INNER JOINs drop products with no order_items. Which JOIN type keeps all products?",
        "explanation": "Change both JOINs to LEFT JOINs. INNER JOIN drops products with no matching order_items. LEFT JOIN keeps all products, and COALESCE turns the resulting NULL sum into 0.",
    },
]
