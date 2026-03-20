exercise = {
    "title": "CTEs (WITH clause) — multi-step analysis",
    "description": "Top 5 customers by revenue using chained CTEs (like pipeline stages).",
    "queries": {
        "Chained CTEs": """
WITH order_revenue AS (
    SELECT o.id AS order_id,
           o.customer_id,
           SUM(oi.quantity * p.price) AS order_total
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    WHERE o.status = 'completed'
    GROUP BY o.id, o.customer_id
),
customer_summary AS (
    SELECT c.name AS customer,
           c.segment,
           COUNT(r.order_id) AS completed_orders,
           ROUND(SUM(r.order_total), 2) AS total_revenue,
           ROUND(AVG(r.order_total), 2) AS avg_order_value
    FROM customers c
    LEFT JOIN order_revenue r ON c.id = r.customer_id
    GROUP BY c.id, c.name, c.segment
)
SELECT customer, segment, completed_orders, total_revenue, avg_order_value
FROM customer_summary
ORDER BY total_revenue DESC
LIMIT 5;""",
    },
    "explanation": """
CTEs break complex queries into named steps — like functions in code:
  1. order_revenue  — calculate each order's total (Bronze -> Silver)
  2. customer_summary — aggregate per customer    (Silver -> Gold)
  3. Final SELECT — pick the top 5                (Gold -> Report)

This mirrors the Medallion Architecture used in real data pipelines.
"""
}
