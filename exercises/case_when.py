exercise = {
    "title": "CASE WHEN + conditional aggregation",
    "description": "Pivot-style summary: order counts by status per customer.",
    "queries": {
        "Conditional counts": """
SELECT c.name AS customer,
       COUNT(*) AS total_orders,
       SUM(CASE WHEN o.status = 'completed' THEN 1 ELSE 0 END) AS completed,
       SUM(CASE WHEN o.status = 'pending' THEN 1 ELSE 0 END) AS pending,
       SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled,
       ROUND(SUM(CASE WHEN o.status = 'completed' THEN 1 ELSE 0 END) * 100.0
             / COUNT(*), 0) || '%' AS completion_rate
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.name
ORDER BY total_orders DESC;""",
    },
    "explanation": """
CASE WHEN inside aggregate functions = pivot tables in SQL.
Each CASE acts as a conditional counter/summer.

Pattern:  SUM(CASE WHEN condition THEN value ELSE 0 END)
This is extremely common in reporting queries.
"""
}
