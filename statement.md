# Problem Statement


## Problem Statement

Most students study wrong in a way that isn't optimal, often not out of laziness but simply because no one taught them differently. They cram by re-reading notes a day or two before the exam, spend equal time on topics that they understand well as topics that they struggled to learn, and within only a week have forgotten most of what they 'learned'. Spaced repetition and prioritized planning are known to be effective solutions but require multiple different apps, each of which has no knowledge of the user's exams and topics. This project aims to solve both of these problems with a single tool.


## Scope of the Project

In scope

- Subject tracking (with exam dates) and topic tracking (with difficulty levels)

- Daily, prioritized study planner

- Flashcards with the SM-2 spaced repetition algorithm determining the next review date

- Tracking streaks, average recall, weak topics, a calculated exam-readiness rate, and various other statistics

- Persistent local storage (SQLite), CSV export, logging, validation, and automated testing

Out of scope

- Multi-user accounts or syncing with external calendars or services

- Automatic card generation

- Native mobile or web application

## Target Users

- University students (ideally first-year engineering students) studying a number of different subjects

- Self-learners studying for an exam or certification

- People looking for a convenient, no-account-needed, offline tool for learning

## High-Level Features

1. Study Planner

- Planning of subjects and topics with difficulty levels

- Daily, topic-based planner that prioritizes topics based on difficulty and planned study time per day

2. Flashcards / Spaced Repetition System

- Creation of flashcards

- Reviewing of flashcards with 0-5 recall rating, next review estimated with SM-2 algorithm

3. Progress Analytics

- Tracking of daily streaks, average recall, weak topics

- Exam-readiness estimator

- Statistics visualized in graphs

4. Data Persistence

- Local storage using SQLite

- Exporting of data to CSV files

- Cascading deletes for proper database maintenance

5. Quality Assurance

- Input validation and error handling

- Logging system that rotates logs daily

- 71 automated unit tests
