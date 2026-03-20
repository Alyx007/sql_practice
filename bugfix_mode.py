"""Fix-the-bug mode — find and fix errors in broken SQL queries."""

from .db import fetch_query, print_result, results_match, run_query, read_sql_input


def run_bugfix_mode(conn, bugs):
    total = len(bugs)

    print("\n" + "="*70)
    print("  FIX THE BUG MODE")
    print("  Each challenge shows a broken query. Fix it! Commands:")
    print("    hint     — get a clue about what's wrong")
    print("    run      — run the buggy query to see its (wrong) output")
    print("    skip     — move to next bug")
    print("    solution — show the fix")
    print("    quit     — exit")
    print("="*70)

    fixed = 0

    for i, bug in enumerate(bugs, 1):
        print(f"\n{'─'*70}")
        print(f"  Bug {i}/{total}")
        print(f"  {bug['title']}")
        print(f"{'─'*70}")
        print(f"\n{bug['description']}\n")
        print(f"  Buggy query:\033[31m\n{bug['buggy_sql']}\033[0m\n")

        while True:
            try:
                user_input = read_sql_input("FIX> ")
            except (EOFError, KeyboardInterrupt):
                print(f"\n\nFinished! You fixed {fixed}/{total} bugs.")
                return

            if user_input in ("quit", "q"):
                print(f"\nFinished! You fixed {fixed}/{total} bugs.")
                return

            if user_input == "skip":
                print("  Skipped.")
                break

            if user_input == "hint":
                print(f"\n  Hint: {bug['hint']}\n")
                continue

            if user_input == "run":
                print("  Buggy output:")
                run_query(conn, bug["buggy_sql"])
                print("  ^ This is WRONG. Your job is to fix the query.\n")
                continue

            if user_input == "solution":
                print(f"\n  Fixed SQL:\033[32m\n{bug['expected_sql']}\033[0m")
                print("\n  Explanation: " + bug.get("explanation", bug["hint"]))
                exp_res = fetch_query(conn, bug["expected_sql"])
                if exp_res[0] is not None:
                    print("\n  Correct result:")
                    print_result(*exp_res)
                break

            # User submitted fix — compare
            match, user_res, exp_res, error = results_match(conn, user_input, bug["expected_sql"])

            if error:
                print(f"\n  SQL Error: {error}")
                print("  Still broken! Try again or type 'hint'.\n")
                continue

            print("  Your result:")
            print_result(*user_res)

            if match:
                fixed += 1
                print(f"  \033[32mFixed!\033[0m ({fixed}/{total} done)\n")
                break
            else:
                print("  \033[31mNot the right fix.\033[0m Expected result:")
                print_result(*exp_res)
                print("  Try again, or type 'hint'.\n")

    print(f"\nBug hunt complete! You fixed {fixed}/{total} bugs.")
