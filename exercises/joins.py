exercise = {
    "title": "LEFT JOIN vs RIGHT JOIN vs INNER JOIN",
    "description": "See which employees/departments appear or disappear with each join type.",
    "queries": {
        "INNER JOIN (only matches)": """
SELECT e.name AS employee, e.dept_id, d.name AS department
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id
ORDER BY d.name, e.name;""",

        "LEFT JOIN (all employees, even without dept)": """
SELECT e.name AS employee, e.dept_id, d.name AS department
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id
ORDER BY d.name, e.name;""",

        "RIGHT JOIN (all depts — rewritten as swapped LEFT JOIN for SQLite)": """
SELECT e.name AS employee, d.id AS dept_id, d.name AS department
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.id
ORDER BY d.name, e.name;""",
    },
    "explanation": """
COMPARE THE RESULTS:
  INNER JOIN: 12 rows — Karen, Leo (NULL dept), Mona (dept 99), and Legal dept ALL gone.
  LEFT JOIN:  15 rows — ALL employees kept. Karen/Leo/Mona show NULL department.
              Legal gone (no employee references it).
  RIGHT JOIN: 13 rows — ALL departments kept. Legal appears with NULL employee.
              Karen, Leo, Mona gone (their dept_id doesn't match any department).

KEY INSIGHT: "LEFT" = the FROM table. "RIGHT" = the JOIN table.
"""
}
