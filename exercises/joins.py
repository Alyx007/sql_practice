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
""",
    "questions": [
        {
            "question": "An employee has dept_id = NULL. Which JOIN type will STILL include them in the result?",
            "options": ["A) INNER JOIN", "B) LEFT JOIN (employees LEFT JOIN departments)", "C) RIGHT JOIN (employees RIGHT JOIN departments)", "D) None of the above"],
            "answer": "B",
            "explanation": "LEFT JOIN keeps ALL rows from the left (FROM) table, even when there's no match. INNER JOIN drops them, RIGHT JOIN keeps all from the right table.",
        },
        {
            "question": "The Legal department has no employees. Which query returns a row for Legal?",
            "options": ["A) SELECT * FROM employees e INNER JOIN departments d ON e.dept_id = d.id", "B) SELECT * FROM employees e LEFT JOIN departments d ON e.dept_id = d.id", "C) SELECT * FROM departments d LEFT JOIN employees e ON e.dept_id = d.id", "D) Both A and B"],
            "answer": "C",
            "explanation": "Only when departments is the LEFT (preserved) table will Legal appear. In A and B, departments is the right table, so unmatched departments are dropped.",
        },
        {
            "question": "Mona has dept_id = 99, which doesn't exist in departments. What does INNER JOIN return for her?",
            "options": ["A) A row with NULL department name", "B) A row with department name '99'", "C) Nothing — she is excluded", "D) An error"],
            "answer": "C",
            "explanation": "INNER JOIN only returns rows where the ON condition finds a match. Since dept_id=99 has no match in departments, Mona is excluded entirely.",
        },
    ],
}
