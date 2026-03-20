challenges = [
    {
        "title": "Department salary stats",
        "difficulty": "easy",
        "description": (
            "For each department, show: department name, employee count,\n"
            "average salary (rounded to 0 decimals), and max salary.\n"
            "Only include departments with more than 2 employees.\n"
            "Order by average salary descending."
        ),
        "expected_sql": """
SELECT d.name AS department,
       COUNT(e.id) AS emp_count,
       ROUND(AVG(e.salary), 0) AS avg_salary,
       MAX(e.salary) AS max_salary
FROM employees e
JOIN departments d ON e.dept_id = d.id
GROUP BY d.name
HAVING COUNT(e.id) > 2
ORDER BY avg_salary DESC;""",
        "hints": [
            "GROUP BY department, then use aggregate functions (COUNT, AVG, MAX).",
            "To filter groups, you need HAVING (not WHERE — WHERE runs before grouping).",
            "HAVING COUNT(e.id) > 2 keeps only departments with more than 2 employees.",
        ],
    },
    {
        "title": "Top 3 customers by order count",
        "difficulty": "easy",
        "description": (
            "Find the top 3 customers by number of completed orders.\n"
            "Show customer name and their completed order count.\n"
            "Only count orders with status = 'completed'."
        ),
        "expected_sql": """
SELECT c.name, COUNT(o.id) AS completed_orders
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE o.status = 'completed'
GROUP BY c.name
ORDER BY completed_orders DESC
LIMIT 3;""",
        "hints": [
            "Filter completed orders with WHERE, then GROUP BY customer.",
            "WHERE filters rows before grouping. Use it for status = 'completed'.",
            "ORDER BY the count DESC and LIMIT 3 for top 3.",
        ],
    },
    {
        "title": "Revenue per product category",
        "difficulty": "medium",
        "description": (
            "Calculate total revenue per product category.\n"
            "Revenue = quantity * price. Only include completed orders.\n"
            "Show category, total_revenue (rounded to 2 decimals), and items_sold.\n"
            "Order by total_revenue descending."
        ),
        "expected_sql": """
SELECT p.category,
       ROUND(SUM(oi.quantity * p.price), 2) AS total_revenue,
       SUM(oi.quantity) AS items_sold
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
JOIN products p ON oi.product_id = p.id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY total_revenue DESC;""",
        "hints": [
            "You need to join 3 tables: order_items, orders (for status filter), and products (for price and category).",
            "Revenue per item = oi.quantity * p.price. SUM that up per category.",
            "Filter WHERE o.status = 'completed' before grouping by p.category.",
        ],
    },
    {
        "title": "Order status breakdown per customer",
        "difficulty": "medium",
        "description": (
            "Build a pivot-style table showing each customer's name,\n"
            "total orders, and counts for each status (completed, pending, cancelled).\n"
            "Order by total_orders descending."
        ),
        "expected_sql": """
SELECT c.name,
       COUNT(*) AS total_orders,
       SUM(CASE WHEN o.status = 'completed' THEN 1 ELSE 0 END) AS completed,
       SUM(CASE WHEN o.status = 'pending' THEN 1 ELSE 0 END) AS pending,
       SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.name
ORDER BY total_orders DESC;""",
        "hints": [
            "You need CASE WHEN inside an aggregate to count conditionally.",
            "SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) counts completed orders.",
            "Do this for each status and GROUP BY customer name.",
        ],
    },
]
