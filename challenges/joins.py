challenges = [
    {
        "title": "Employees without a valid department",
        "difficulty": "easy",
        "description": (
            "List the name and dept_id of every employee who has NO matching\n"
            "department (either NULL dept_id or a dept_id that doesn't exist).\n"
            "Order by name."
        ),
        "expected_sql": """
SELECT e.name, e.dept_id
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id
WHERE d.id IS NULL
ORDER BY e.name;""",
        "hints": [
            "Which JOIN type keeps ALL rows from the left table, even without a match?",
            "Use LEFT JOIN, then filter for rows where the right side is NULL.",
            "WHERE d.id IS NULL gives you employees whose dept_id had no match.",
        ],
    },
    {
        "title": "Departments with their employee count",
        "difficulty": "easy",
        "description": (
            "List ALL departments with their employee count.\n"
            "Departments with no employees should show 0.\n"
            "Order by department name."
        ),
        "expected_sql": """
SELECT d.name AS department, COUNT(e.id) AS employee_count
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.id
GROUP BY d.name
ORDER BY d.name;""",
        "hints": [
            "You need ALL departments, even empty ones. Which table should be on the LEFT?",
            "LEFT JOIN from departments to employees keeps all departments.",
            "Use COUNT(e.id) not COUNT(*) — COUNT(e.id) ignores NULLs, giving 0 for empty depts.",
        ],
    },
    {
        "title": "Customers who never ordered",
        "difficulty": "easy",
        "description": (
            "Find the name, city, and segment of customers who have\n"
            "never placed any order. This is the 'anti-join' pattern."
        ),
        "expected_sql": """
SELECT c.name, c.city, c.segment
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;""",
        "hints": [
            "LEFT JOIN keeps all customers. What's NULL when there's no matching order?",
            "After the LEFT JOIN, filter WHERE o.id IS NULL to find customers with no orders.",
        ],
    },
    {
        "title": "Employees with their manager's name",
        "difficulty": "medium",
        "description": (
            "List every employee's name, their salary, and their manager's name.\n"
            "If they have no manager, show 'Top Level' instead.\n"
            "Order by manager name, then employee name."
        ),
        "expected_sql": """
SELECT e.name, e.salary, COALESCE(m.name, 'Top Level') AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id
ORDER BY manager, e.name;""",
        "hints": [
            "This is a self-join — joining a table to itself.",
            "LEFT JOIN employees m ON e.manager_id = m.id links each employee to their manager.",
            "Use COALESCE(m.name, 'Top Level') to replace NULL manager names.",
        ],
    },
]
