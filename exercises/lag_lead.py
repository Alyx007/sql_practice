exercise = {
    "title": "LAG / LEAD — comparing rows over time",
    "description": "Calculate month-over-month revenue change.",
    "queries": {
        "Month-over-month with LAG": """
WITH monthly AS (
    SELECT strftime('%Y-%m', o.order_date) AS month,
           ROUND(SUM(oi.quantity * p.price), 2) AS revenue
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    WHERE o.status = 'completed'
    GROUP BY strftime('%Y-%m', o.order_date)
)
SELECT month,
       revenue,
       LAG(revenue) OVER (ORDER BY month) AS prev_month,
       ROUND(revenue - LAG(revenue) OVER (ORDER BY month), 2) AS change,
       CASE
           WHEN LAG(revenue) OVER (ORDER BY month) IS NULL THEN 'N/A'
           ELSE ROUND((revenue - LAG(revenue) OVER (ORDER BY month))
                      / LAG(revenue) OVER (ORDER BY month) * 100, 1) || '%'
       END AS growth
FROM monthly
ORDER BY month;""",
    },
    "explanation": """
LAG(column, N) looks N rows BACK.  LEAD(column, N) looks N rows FORWARD.
Default N = 1. First row's LAG is always NULL (no previous row).

Essential for: time-series analysis, detecting trends, calculating deltas.
"""
}
