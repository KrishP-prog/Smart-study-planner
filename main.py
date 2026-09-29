#Smart Study Planner

#Run with:  python main.py

from __future__ import annotations

import sqlite3

from src import analytics, database, exporter, flashcards, planner
from src.errors import StudyPlannerError, ValidationError
from src.logger import get_logger

log = get_logger("main")

#This is the main menu after running of the code

MENU = """
============== Smart Study Planner ==============
  1. Add subject              7. Review due flashcards
  2. List subjects            8. Show study plan
  3. Add topic                9. Progress & analytics
  4. List topics             10. Generate charts
  5. Mark topic done         11. Export flashcards (CSV)
  6. Add flashcard           12. Delete subject
  0. Exit
=================================================
"""

def ask(prompt: str) -> str:
    return input(prompt).strip()

#Subject

def cmd_add_subject(conn) -> None:
    name = ask("Subject name: ")
    exam = ask("Exam date (YYYY-MM-DD): ")
    subject = planner.add_subject(conn, name, exam)
    print(f"Added '{subject.name}' (id {subject.id}), exam on {subject.exam_date}.")

def cmd_list_subjects(conn) -> None:
    subjects = planner.list_subjects(conn)
    if not subjects:
        print("No subjects yet. Add one first.")
        return
    for s in subjects:
        print(f"  [{s.id}] {s.name:<25} exam: {s.exam_date}")

#Topic

def cmd_add_topic(conn) -> None:
    cmd_list_subjects(conn)
    subject_id = ask("Subject ID: ")
    name = ask("Topic name: ")
    difficulty = ask("Difficulty 1 (easy) - 5 (very hard) [3]: ") or "3"
    topic = planner.add_topic(conn, subject_id, name, difficulty)
    print(f"Added topic '{topic.name}' (id {topic.id}).")

def cmd_list_topics(conn) -> None:
    topics = planner.list_topics(conn)
    if not topics:
        print("No topics yet.")
        return
    for t in topics:
        mark = "x" if t.status == "done" else " "
        print(f"  [{t.id}] ({mark}) subject {t.subject_id} | {t.name} | difficulty {t.difficulty}")

def cmd_mark_done(conn) -> None:
    cmd_list_topics(conn)
    topic_id = ask("Topic ID to mark done: ")
    topic = planner.set_topic_status(conn, topic_id, "done")
    print(f"'{topic.name}' marked as done.")

def cmd_add_card(conn) -> None:
    cmd_list_topics(conn)
    topic_id = ask("Topic ID for this card: ")
    question = ask("Question: ")
    answer = ask("Answer: ")
    card = flashcards.add_card(conn, topic_id, question, answer)
    print(f"Card {card.id} added. It is due today.")

#Flashcards

def cmd_review(conn) -> None:
    due = flashcards.get_due_cards(conn)
    if not due:
        print("No cards due right now. Nice work!")
        return
    print(f"{len(due)} card(s) due. Enter 'q' at the rating prompt to stop.")
    for i, card in enumerate(due, start=1):
        print(f"\nCard {i}/{len(due)}\nQ: {card.question}")
        ask("Press Enter to reveal the answer... ")
        print(f"A: {card.answer}")
        while True:
            raw = ask("Rate recall 0 (blackout) to 5 (perfect), or q to quit: ")
            if raw.lower() == "q":
                print("Review session ended.")
                return
            try:
                updated = flashcards.review_card(conn, card.id, raw)
                break
            except ValidationError as exc:
                print(f"  {exc}")
        print(f"  Next review: {updated.next_review} (in {updated.interval} day(s))")
    print("\nAll due cards reviewed. Great job!")

def cmd_plan(conn) -> None:
    days = ask("How many days to plan? [7]: ") or "7"
    for day_plan in planner.generate_schedule(conn, days=days):
        print(f"\n{day_plan.day.strftime('%a %d %b %Y')}  -  {day_plan.cards_due} card(s) due")
        if not day_plan.topics:
            print("   (no new topics)")
        for n, p in enumerate(day_plan.topics, start=1):
            print(f"   {n}. [{p.subject_name}] {p.name} "
                  f"(difficulty {p.difficulty}, priority {p.priority:.2f})")

def cmd_analytics(conn) -> None:
    s = analytics.summary(conn)
    avg = "n/a" if s["average_quality"] is None else s["average_quality"]
    print(f"\nTotal cards: {s['total_cards']} | Due now: {s['due_today']} | "
          f"Reviews done: {s['total_reviews']}")
    print(f"Average recall quality: {avg} | Current streak: {s['streak']} day(s)")

    subjects = planner.list_subjects(conn)
    if subjects:
        print("\nExam readiness:")
        for subj in subjects:
            print(f"  {subj.name:<25} {analytics.exam_readiness(conn, subj.id):>5.1f} / 100")

    weak = analytics.weak_topics(conn)
    if weak:
        print("\nWeakest topics (lowest average recall):")
        for subject, topic, avg_q in weak:
            print(f"  {subject} > {topic}: {avg_q}")

#Charts

def cmd_charts(conn) -> None:
    paths = analytics.plot_charts(conn)
    print("Charts saved:")
    for p in paths:
        print(f"  {p}")

def cmd_export(conn) -> None:
    path = ask("Export file [data/flashcards.csv]: ") or "data/flashcards.csv"
    count = exporter.export_cards_csv(conn, path)
    print(f"Exported {count} card(s) to {path}.")

def cmd_delete_subject(conn) -> None:
    cmd_list_subjects(conn)
    subject_id = ask("Subject ID to delete: ")
    subject = planner.get_subject(conn, subject_id)
    confirm = ask(f"Delete '{subject.name}' with all its topics and cards? (y/n): ")
    if confirm.lower() == "y":
        planner.delete_subject(conn, subject.id)
        print("Deleted.")
    else:
        print("Cancelled.")

#Actions

ACTIONS = {
    "1": cmd_add_subject, "2": cmd_list_subjects, "3": cmd_add_topic,
    "4": cmd_list_topics, "5": cmd_mark_done, "6": cmd_add_card,
    "7": cmd_review, "8": cmd_plan, "9": cmd_analytics,
    "10": cmd_charts, "11": cmd_export, "12": cmd_delete_subject,
}

#Exit Options

def run(conn: sqlite3.Connection) -> None:
    """Main menu loop. Errors are reported, never crash the program."""
    while True:
        print(MENU)
        choice = ask("Choose an option: ")
        if choice == "0":
            print("Goodbye! Keep studying.")
            return
        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid option. Please choose a number from the menu.")
            continue
        try:
            action(conn)
        except StudyPlannerError as exc:
            log.warning("%s failed: %s", action.__name__, exc)
            print(f"Error: {exc}")
        except sqlite3.Error as exc:
            log.exception("Database error in %s", action.__name__)
            print(f"Database error: {exc}")

def main() -> int:
    try:
        conn = database.get_connection()
    except StudyPlannerError as exc:
        print(f"Startup failed: {exc}")
        return 1
    try:
        run(conn)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
    finally:
        conn.close()
    return 0

#Exit

if __name__ == "__main__":
    raise SystemExit(main())