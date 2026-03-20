exercise = {
    "title": "Window functions: ROW_NUMBER, RANK, running totals",
    "description": "Rank employees by salary within each department + compute running totals.",
    "queries": {
        "ROW_NUMBER (rank within department)": """
SELECT e.name, d.name AS dept, e.salary,
       ROW_NUMBER() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS rank_in_dept
FROM employees e
JOIN departments d ON e.dept_id = d.id
ORDER BY d.name, rank_in_dept;""",

        "Running total of salaries": """
SELECT e.name, e.salary,
       SUM(e.salary) OVER (ORDER BY e.salary DESC) AS running_total,
       ROUND(SUM(e.salary) OVER (ORDER BY e.salary DESC) * 100.0 /
             (SELECT SUM(salary) FROM employees), 1) AS cumulative_pct
FROM employees e
ORDER BY e.salary DESC;""",
    },
    "explanation": """
Window functions compute across rows WITHOUT collapsing them (unlike GROUP BY).
  PARTITION BY = reset the calculation for each group
  ORDER BY inside OVER() = in what order to process rows

ROW_NUMBER: always unique (1,2,3)
RANK:       ties share rank, gaps after (1,1,3)
DENSE_RANK: ties share rank, no gaps   (1,1,2)
""",
    "questions": [
        {
            "question": "Three employees have the same salary. What does RANK() assign them?",
            "options": ["A) 1, 2, 3", "B) 1, 1, 1 (next is 4)", "C) 1, 1, 1 (next is 2)", "D) 1, 2, 3 (randomly)"],
            "answer": "B",
            "explanation": "RANK gives tied rows the same rank, then skips ahead. So three ties at rank 1 means the next rank is 4. DENSE_RANK would give 1,1,1,2 instead.",
        },
        {
            "question": "What does PARTITION BY do in a window function?",
            "options": ["A) Filters rows like WHERE", "B) Groups rows and collapses them like GROUP BY", "C) Resets the window calculation for each group, keeping all rows", "D) Sorts the final output"],
            "answer": "C",
            "explanation": "PARTITION BY divides rows into groups for the window calculation, but unlike GROUP BY, it does NOT collapse rows — every original row is still in the result.",
        },
        {
            "question": "What is the key difference between window functions and GROUP BY?",
            "options": ["A) Window functions are faster", "B) GROUP BY keeps all rows, window functions collapse them", "C) Window functions keep all rows, GROUP BY collapses them into groups", "D) There is no difference"],
            "answer": "C",
            "explanation": "GROUP BY reduces multiple rows into one per group. Window functions compute values across rows but return every original row in the result.",
        },
    ],
}
