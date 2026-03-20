"""
SQL Practice Environment — run with:  python3 -m sql_practice

Modes:
  1) Guided exercises — read, run, and learn from explained queries
  2) Interactive SQL — free-form sandbox to write your own queries
  3) Practice mode — solve challenges with progressive hints
  4) Fix the bug — find and fix errors in broken queries
  5) All modes in sequence
"""

from .db import connect, run_query
from .data.schema import load_seed, show_tables
from .exercises import ALL as exercises
from .challenges import ALL as challenges
from .bugs import ALL as bugs
from .practice_mode import run_practice_mode
from .bugfix_mode import run_bugfix_mode


def run_exercise(conn, exercise):
    print(f"\n{'='*70}")
    print(f"  EXERCISE: {exercise['title']}")
    print(f"  {exercise['description']}")
    print(f"{'='*70}")

    for label, sql in exercise["queries"].items():
        print(f"\n--- {label} ---")
        print(f"\033[36m{sql}\033[0m")
        run_query(conn, sql)

    print(exercise["explanation"])

    # Quiz questions
    questions = exercise.get("questions", [])
    if not questions:
        return

    correct = 0
    print(f"  --- Quiz: {len(questions)} questions ---\n")

    for qi, q in enumerate(questions, 1):
        print(f"  Q{qi}. {q['question']}")
        for opt in q["options"]:
            print(f"      {opt}")

        while True:
            try:
                answer = input("\n  Your answer (A/B/C/D): ").strip().upper()
            except (EOFError, KeyboardInterrupt):
                print()
                return
            if answer in ("A", "B", "C", "D"):
                break
            print("  Please enter A, B, C, or D.")

        if answer == q["answer"]:
            correct += 1
            print(f"  \033[32mCorrect!\033[0m {q['explanation']}\n")
        else:
            print(f"  \033[31mWrong.\033[0m The answer is {q['answer']}. {q['explanation']}\n")

    print(f"  Score: {correct}/{len(questions)}")


def show_help():
    print("\n--- Quick SQL Reference ---\n")
    print("  Filtering:     SELECT * FROM employees WHERE salary > 70000;")
    print("  Sorting:       SELECT * FROM employees ORDER BY salary DESC;")
    print("  Joins:         SELECT e.name, d.name FROM employees e LEFT JOIN departments d ON e.dept_id = d.id;")
    print("  Grouping:      SELECT dept_id, AVG(salary) FROM employees GROUP BY dept_id;")
    print("  Having:        ... GROUP BY dept_id HAVING COUNT(*) > 2;")
    print("  Window:        SELECT name, salary, ROW_NUMBER() OVER (ORDER BY salary DESC) FROM employees;")
    print("  CTE:           WITH top AS (SELECT * FROM employees WHERE salary > 80000) SELECT * FROM top;")
    print("  Nulls:         SELECT * FROM employees WHERE dept_id IS NULL;")
    print("  Coalesce:      SELECT COALESCE(dept_id, 0) FROM employees;")
    print("  Case:          SELECT CASE WHEN salary > 80000 THEN 'Senior' ELSE 'Junior' END FROM employees;")
    print()


def interactive_mode(conn):
    print("\n" + "="*70)
    print("  INTERACTIVE SQL MODE")
    print("  Type any SQL query ending with ; and press Enter.")
    print("  Commands:  'tables'  'help'  'quit'")
    print("="*70 + "\n")

    while True:
        try:
            lines = []
            prompt = "SQL> "
            while True:
                line = input(prompt)
                if line.lower() in ("quit", "exit", "q"):
                    return
                if line.lower() == "tables":
                    show_tables()
                    break
                if line.lower() == "help":
                    show_help()
                    break
                lines.append(line)
                if line.strip().endswith(";"):
                    run_query(conn, " ".join(lines))
                    lines = []
                    break
                prompt = "...> "
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            return


def run_guided_exercises(conn):
    for ex in exercises:
        run_exercise(conn, ex)
        input("\nPress Enter for next exercise...")


def main():
    print("\n" + "="*70)
    print("  SQL PRACTICE ENVIRONMENT")
    print("="*70)

    conn = connect()
    load_seed(conn)
    print("\nDatabase ready — 6 tables loaded.\n")
    show_tables()

    while True:
        print("OPTIONS:")
        print("  1) Guided exercises    — 7 topics with queries + quiz")
        print("  2) Interactive SQL     — free sandbox, write anything")
        print("  3) Practice mode       — solve challenges with hints  [14 challenges]")
        print("  4) Fix the bug         — find errors in broken SQL    [9 bugs]")
        print("  5) Full session        — all modes in sequence")
        print("  q) Quit\n")

        try:
            choice = input("Choose [1/2/3/4/5/q]: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if choice in ("q", "Q"):
            break
        elif choice == "1":
            run_guided_exercises(conn)
        elif choice == "2":
            interactive_mode(conn)
        elif choice == "3":
            run_practice_mode(conn, challenges)
        elif choice == "4":
            run_bugfix_mode(conn, bugs)
        elif choice == "5":
            print("\n--- Starting with guided exercises ---")
            run_guided_exercises(conn)
            print("\n--- Now: practice challenges ---")
            run_practice_mode(conn, challenges)
            print("\n--- Now: fix the bug ---")
            run_bugfix_mode(conn, bugs)
            print("\n--- Finally: free sandbox ---")
            interactive_mode(conn)
        else:
            print("  Invalid choice, try again.\n")
            continue

        print()

    conn.close()
    print("Done!")


if __name__ == "__main__":
    main()
