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
""",
    "questions": [
        {
            "question": "What does the WITH clause define?",
            "options": ["A) A permanent table in the database", "B) A temporary named result set (CTE) that exists only for the query", "C) A view that persists after the query", "D) A stored procedure"],
            "answer": "B",
            "explanation": "CTEs (Common Table Expressions) are temporary, named result sets that only exist for the duration of the query. They're not stored anywhere.",
        },
        {
            "question": "Can a CTE reference another CTE defined before it in the same WITH clause?",
            "options": ["A) No, CTEs are independent", "B) Yes, as long as the referenced CTE is defined earlier", "C) Only if you use a subquery instead", "D) Only in PostgreSQL, not SQLite"],
            "answer": "B",
            "explanation": "CTEs can be chained — a later CTE can reference an earlier one. This is what makes them powerful for multi-step transformations, like a pipeline.",
        },
        {
            "question": "Why use a CTE instead of a subquery?",
            "options": ["A) CTEs are always faster", "B) CTEs can be indexed", "C) CTEs improve readability by giving names to intermediate steps", "D) Subqueries are deprecated in modern SQL"],
            "answer": "C",
            "explanation": "The main benefit of CTEs is readability. They let you name and separate logical steps instead of nesting subqueries deeply. Performance is usually the same.",
        },
    ],
}
