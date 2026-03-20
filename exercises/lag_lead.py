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
""",
    "questions": [
        {
            "question": "What does LAG(revenue) return for the FIRST row in the result?",
            "options": ["A) 0", "B) The same row's revenue", "C) NULL", "D) An error"],
            "answer": "C",
            "explanation": "There is no previous row for the first row, so LAG returns NULL. You can provide a default: LAG(revenue, 1, 0) to return 0 instead.",
        },
        {
            "question": "You want to compare each row with the row TWO positions ahead. Which function do you use?",
            "options": ["A) LAG(column, 2)", "B) LEAD(column, 2)", "C) LAG(column, -2)", "D) NEXT(column, 2)"],
            "answer": "B",
            "explanation": "LEAD looks forward. LEAD(column, 2) skips one row and returns the value from two rows ahead. LAG(column, 2) looks two rows back.",
        },
        {
            "question": "LAG and LEAD require which clause to determine row order?",
            "options": ["A) GROUP BY", "B) PARTITION BY", "C) ORDER BY inside OVER()", "D) WHERE"],
            "answer": "C",
            "explanation": "LAG/LEAD need ORDER BY inside OVER() to know which row is 'previous' or 'next'. Without it, the row order is undefined.",
        },
    ],
}
