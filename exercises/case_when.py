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
""",
    "questions": [
        {
            "question": "What does SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) count?",
            "options": ["A) The total number of rows", "B) The number of rows where status is 'completed'", "C) The sum of all status values", "D) 1 or 0 depending on the first row"],
            "answer": "B",
            "explanation": "The CASE returns 1 for each 'completed' row and 0 for everything else. SUM adds these up, effectively counting completed rows.",
        },
        {
            "question": "What happens if you omit the ELSE clause in CASE WHEN?",
            "options": ["A) An error occurs", "B) It defaults to ELSE 0", "C) It defaults to ELSE NULL", "D) It defaults to ELSE ''"],
            "answer": "C",
            "explanation": "Without ELSE, CASE returns NULL for unmatched conditions. This matters with SUM (NULL is ignored) vs COUNT (NULL may or may not be counted depending on usage).",
        },
        {
            "question": "How do you create a pivot-style summary (columns for each status) in SQL?",
            "options": ["A) Use PIVOT keyword", "B) Use multiple SUM(CASE WHEN ... END) columns", "C) Use GROUP BY on each status separately", "D) Use UNION for each status"],
            "answer": "B",
            "explanation": "Standard SQL (and SQLite) doesn't have a PIVOT keyword. The common pattern is one SUM(CASE WHEN ...) per column you want to pivot into.",
        },
    ],
}
