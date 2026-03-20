"""Practice mode — solve SQL challenges with progressive hints."""

from .db import fetch_query, print_result, results_match, read_sql_input


def run_practice_mode(conn, challenges):
    total = len(challenges)

    print("\n" + "="*70)
    print("  PRACTICE MODE")
    print("  Write SQL to solve each challenge. Commands:")
    print("    hint     — reveal next hint (progressive)")
    print("    skip     — move to next challenge")
    print("    solution — show the expected query")
    print("    quit     — exit practice mode")
    print("="*70)

    solved = 0

    for i, ch in enumerate(challenges, 1):
        hint_index = 0
        total_hints = len(ch["hints"])

        print(f"\n{'─'*70}")
        print(f"  Challenge {i}/{total}  [{ch['difficulty'].upper()}]")
        print(f"  {ch['title']}")
        print(f"{'─'*70}")
        print(f"\n{ch['description']}\n")

        while True:
            try:
                user_input = read_sql_input("YOUR SQL> ")
            except (EOFError, KeyboardInterrupt):
                print(f"\n\nFinished! You solved {solved}/{total} challenges.")
                return

            if user_input in ("quit", "q"):
                print(f"\nFinished! You solved {solved}/{total} challenges.")
                return

            if user_input == "skip":
                print("  Skipped.")
                break

            if user_input == "hint":
                if hint_index < total_hints:
                    hint_index += 1
                    print(f"\n  Hint {hint_index}/{total_hints}: {ch['hints'][hint_index - 1]}\n")
                else:
                    print("\n  No more hints. Type 'solution' to see the answer.\n")
                continue

            if user_input == "solution":
                print(f"\n  Expected SQL:\033[36m\n{ch['expected_sql']}\033[0m")
                exp_res = fetch_query(conn, ch["expected_sql"])
                if exp_res[0] is not None:
                    print("  Expected result:")
                    print_result(*exp_res)
                break

            # User submitted SQL — compare results
            match, user_res, exp_res, error = results_match(conn, user_input, ch["expected_sql"])

            if error:
                print(f"\n  SQL Error: {error}")
                print("  Try again, or type 'hint' for help.\n")
                continue

            print("  Your result:")
            print_result(*user_res)

            if match:
                solved += 1
                print(f"  \033[32mCorrect!\033[0m ({solved}/{total} solved)\n")
                break
            else:
                print("  \033[31mNot quite.\033[0m Expected result:")
                print_result(*exp_res)
                print(f"  Try again, type 'hint' ({hint_index}/{total_hints} used), or 'skip'.\n")

    print(f"\nPractice complete! You solved {solved}/{total} challenges.")
