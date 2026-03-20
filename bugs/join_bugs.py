bugs = [
    {
        "title": "Missing departments in report",
        "description": (
            "This query should list ALL departments with their employee count,\n"
            "including departments with zero employees.\n"
            "But Legal department is missing from the output!"
        ),
        "buggy_sql": """
SELECT d.name AS department, COUNT(e.id) AS employee_count
FROM departments d
INNER JOIN employees e ON e.dept_id = d.id
GROUP BY d.name
ORDER BY d.name;""",
        "expected_sql": """
SELECT d.name AS department, COUNT(e.id) AS employee_count
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.id
GROUP BY d.name
ORDER BY d.name;""",
        "hint": "INNER JOIN drops departments that have no matching employees. Which JOIN keeps ALL departments?",
        "explanation": "Change INNER JOIN to LEFT JOIN. LEFT JOIN keeps all rows from the left table (departments) even when there's no match in the right table (employees).",
    },
    {
        "title": "Wrong employee count — duplicated rows",
        "description": (
            "This query should show each customer's name and how many orders they placed.\n"
            "But customers who ordered multiple products per order are showing inflated counts!"
        ),
        "buggy_sql": """
SELECT c.name, COUNT(*) AS order_count
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN order_items oi ON o.id = oi.order_id
GROUP BY c.name
ORDER BY order_count DESC;""",
        "expected_sql": """
SELECT c.name, COUNT(DISTINCT o.id) AS order_count
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN order_items oi ON o.id = oi.order_id
GROUP BY c.name
ORDER BY order_count DESC;""",
        "hint": "Joining to order_items creates multiple rows per order. How do you count unique orders only?",
        "explanation": "Use COUNT(DISTINCT o.id) instead of COUNT(*). The JOIN to order_items multiplies rows (one per item), so COUNT(*) overcounts. DISTINCT counts each order only once.",
    },
    {
        "title": "Employees with no department showing as having one",
        "description": (
            "This query should show every employee with their department name.\n"
            "Employees without a department should show 'Unassigned'.\n"
            "But Karen, Leo, and Mona are missing entirely!"
        ),
        "buggy_sql": """
SELECT e.name, COALESCE(d.name, 'Unassigned') AS department
FROM employees e
JOIN departments d ON e.dept_id = d.id
ORDER BY department, e.name;""",
        "expected_sql": """
SELECT e.name, COALESCE(d.name, 'Unassigned') AS department
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id
ORDER BY department, e.name;""",
        "hint": "The COALESCE is correct, but it never gets a chance to run. Why are those employees dropped before COALESCE sees them?",
        "explanation": "Change JOIN to LEFT JOIN. The INNER JOIN drops employees with no matching department before COALESCE can replace NULL with 'Unassigned'.",
    },
]
