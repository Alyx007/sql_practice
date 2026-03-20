challenges = [
    {
        "title": "Top 3 customers by total revenue",
        "difficulty": "medium",
        "description": (
            "Using CTEs, find the top 3 customers by total revenue\n"
            "(completed orders only). Revenue = quantity * price.\n"
            "Show customer name, segment, total_revenue (rounded to 2 decimals).\n"
            "Order by total_revenue descending."
        ),
        "expected_sql": """
WITH order_totals AS (
    SELECT o.customer_id,
           SUM(oi.quantity * p.price) AS order_revenue
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    WHERE o.status = 'completed'
    GROUP BY o.customer_id
)
SELECT c.name, c.segment, ROUND(ot.order_revenue, 2) AS total_revenue
FROM customers c
JOIN order_totals ot ON c.id = ot.customer_id
ORDER BY total_revenue DESC
LIMIT 3;""",
        "hints": [
            "Break it into steps: first calculate revenue per customer, then join to customer names.",
            "CTE step 1: JOIN orders + order_items + products, filter completed, GROUP BY customer_id.",
            "Final SELECT: join the CTE to customers for names, ORDER BY DESC, LIMIT 3.",
        ],
    },
    {
        "title": "Best-selling product per category",
        "difficulty": "hard",
        "description": (
            "For each product category, find the best-selling product\n"
            "(by total quantity sold, completed orders only).\n"
            "Show category, product name, and total_quantity.\n"
            "Order by category."
        ),
        "expected_sql": """
WITH product_sales AS (
    SELECT p.category, p.name AS product, SUM(oi.quantity) AS total_quantity,
           ROW_NUMBER() OVER (PARTITION BY p.category ORDER BY SUM(oi.quantity) DESC) AS rn
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.id
    JOIN products p ON oi.product_id = p.id
    WHERE o.status = 'completed'
    GROUP BY p.category, p.name
)
SELECT category, product, total_quantity
FROM product_sales
WHERE rn = 1
ORDER BY category;""",
        "hints": [
            "First get total quantity per product (JOIN + GROUP BY). Then rank within each category.",
            "Use ROW_NUMBER() OVER (PARTITION BY category ORDER BY quantity DESC) to rank per category.",
            "Filter WHERE rn = 1 to keep only the top-selling product in each category.",
        ],
    },
    {
        "title": "Customers with above-average spending",
        "difficulty": "hard",
        "description": (
            "Find customers whose total spending (completed orders) is above\n"
            "the average customer spending. Show name, segment, total_spent\n"
            "(rounded to 2 decimals), and the overall average (avg_spent, rounded to 2).\n"
            "Order by total_spent descending."
        ),
        "expected_sql": """
WITH customer_totals AS (
    SELECT o.customer_id,
           SUM(oi.quantity * p.price) AS total_spent
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    WHERE o.status = 'completed'
    GROUP BY o.customer_id
),
avg_spending AS (
    SELECT ROUND(AVG(total_spent), 2) AS avg_spent
    FROM customer_totals
)
SELECT c.name, c.segment,
       ROUND(ct.total_spent, 2) AS total_spent,
       a.avg_spent
FROM customer_totals ct
JOIN customers c ON ct.customer_id = c.id
CROSS JOIN avg_spending a
WHERE ct.total_spent > a.avg_spent
ORDER BY total_spent DESC;""",
        "hints": [
            "Step 1: CTE to get total spending per customer. Step 2: CTE to get the average of those totals.",
            "Use CROSS JOIN to attach the single avg_spent value to every row.",
            "Filter WHERE total_spent > avg_spent in the final SELECT.",
        ],
    },
]
