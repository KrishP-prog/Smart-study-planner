# Smart Study Planner

A Python command-line app, which turns your exam dates and syllabus topics into a prioritised daily study plan and schedules flashcard reviews at the moment you are about to forget them with the SM-2 spaced repetition algorithm.

## Overview

Students usually revise by re-reading everything shortly before exams. This project instead:

1. Prioritises topics by difficulty and how close the exam is.

2. Schedules flashcard reviews with SM-2, so that easy cards appear less often and hard cards more often.

3. Shows progress analytics (study streaks, weak topics, exam-readiness score, charts).


## Features

| Module | What it does |

| Planner | Subjects with exam dates, topics with difficulty (1-5), priority-based N-day schedule |

| Flashcards + SM-2 | Add cards, review due cards with a 0-5 recall rating, automatic next-review dates |

| Analytics | Study streak, average recall quality, weak topics, exam-readiness score (0-100), 3 matplotlib charts |

| Extras | CSV export of all cards, input validation, rotating log file, cascade delete |


## Technologies Used

- Python 3.9+ (standard library: `sqlite3`, `dataclasses`, `datetime`, `logging`, `csv`)

- SQLite for storage

- matplotlib for charts

- pytest for unit tests

- Git / GitHub for version control


## Project Structure

```
study-planner/

├── main.py # CLI menu (entry point)

├── src/

│ ├── errors.py # custom exceptions

│ ├── logger.py # rotating file logger

│ ├── validators.py # input validation

│ ├── database.py # SQLite connection + schema

│ ├── models.py # dataclasses (Subject, Topic, Card, ...)

│ ├── spaced_repetition.py # SM-2 algorithm

│ ├── flashcards.py # card CRUD + review workflow

│ ├── planner.py # subjects, topics, schedule generator

│ ├── analytics.py # streaks, readiness, charts

│ └── exporter.py # CSV export

├── tests/ # 71 pytest tests

├── docs/ # diagrams, requirements, report outline

├── data/ # SQLite database is created here

├── statement.md

├── requirements.txt

└── README.md

```

## Installation & Running

```bash

# 1. Clone the repository

git clone

cd study-planner

# 2. (Optional) create a virtual environment

python -m venv .venv

source .venv/bin/activate # Windows: .venv\Scripts\activate

# 3. Install dependencies

pip install -r requirements.txt

# 4. Run the app

python main.py

```

The database (`data/planner.db`) and log file (`logs/app.log`) are created automatically on first run.


### Typical workflow


1. Add subject (name + exam date) → 2. Add topics with a difficulty →

3. Add flashcards for each topic → 4. Show study plan each morning →

5. Review due flashcards and rate your recall → 6. Check Progress & analytics.


## How the SM-2 Algorithm Works

After each review you rate your recall from 0 (blackout) to 5 (perfect).


- Rating < 3 → the card restarts: next review in 1 day.

- Rating ≥ 3 → interval grows: 1 day → 6 days → previous interval × ease factor.

- The ease factor (starts at 2.5, never below 1.3) rises for easy cards and falls for hard ones.


Schedule priority: `priority = difficulty / days_left_until_exam`. Higher priority topics are

placed on the earliest days, and a topic is never scheduled after its own exam date.


## Testing

```bash

pytest # run all tests

pytest -v # verbose

```

Tests cover the SM-2 maths, validators, planner/scheduler, flashcard workflow, analytics and CSV

export. Each test uses a fresh in-memory SQLite database, so tests never touch your real data.



## Screenshots


_Add screenshots here (menu, study plan, review session, analytics, charts from `docs/charts/`)._

<img width="432" height="212" alt="Screenshot 2026-09-29 165446" src="https://github.com/user-attachments/assets/4f4a55df-389f-412b-ac60-6a9fde3d79b2" />

<img width="300" height="426" alt="Screenshot 2026-09-29 165802" src="https://github.com/user-attachments/assets/d6cea397-b0c9-47b1-b9c3-a820103ebe5d" />

<img width="422" height="157" alt="Screenshot 2026-09-29 165909" src="https://github.com/user-attachments/assets/6a6acde2-b807-4fd5-9a95-be700e782c04" />


## Non-Functional Highlights

- Security: parameterised SQL queries only (no string-built SQL), strict input validation

- Reliability: custom exceptions, errors never crash the menu loop, foreign keys enforced

- Usability: numbered menu, clear prompts and error messages

- Maintainability: one responsibility per module, docstrings, unit tests

- Logging: all actions and errors written to `logs/app.log` (rotating)


## Future Enhancements

Web/GUI front end, notifications, import cards from CSV, per-topic time estimates, multi-user accounts.
