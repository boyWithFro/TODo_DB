#!/usr/bin/env python3

import sqlite3
import time

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

# create table (updated)
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    date TEXT,
    time TEXT,
    deadline_date TEXT,
    deadline_time TEXT,
    done INTEGER
)
""")
conn.commit()


def add_task():
    desc = input("Enter task: ")
    date = time.strftime("%Y-%m-%d")
    t = time.strftime("%H:%M:%S")

    # deadline input
    deadline_date = input("Enter deadline date (YYYY-MM-DD) or leave empty: ")
    deadline_time = input("Enter deadline time (HH:MM:SS) or leave empty: ")

    if deadline_date == "":
        deadline_date = None
    if deadline_time == "":
        deadline_time = None

    cursor.execute("""
    INSERT INTO tasks (description, date, time, deadline_date, deadline_time, done)
    VALUES (?, ?, ?, ?, ?, 0)
    """, (desc, date, t, deadline_date, deadline_time))
    conn.commit()


def show_tasks():
    cursor.execute("""
    SELECT id, description, date, time, deadline_date, deadline_time, done 
    FROM tasks
    """)
    rows = cursor.fetchall()

    print("\nTasks:")
    for row in rows:
        status = "✓" if row[6] else "✗"

        deadline = ""
        if row[4] and row[5]:
            deadline = f" | Deadline: {row[4]} {row[5]}"
        elif row[4]:
            deadline = f" | Deadline: {row[4]}"

        print(f"{row[0]}: {row[1]} ({row[2]} {row[3]}){deadline} [{status}]")


def mark_done():
    show_tasks()
    task_id = input("\nEnter task ID to mark as done: ")

    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    if cursor.fetchone():
        cursor.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        conn.commit()
    else:
        print("Task not found")


# main loop
while True:
    print("\n1: Add task")
    print("2: Show tasks")
    print("3: Mark task as done")
    print("4: Exit")

    choice = input("Choose: ")

    if choice == "1":
        add_task()
    elif choice == "2":
        show_tasks()
    elif choice == "3":
        mark_done()
    elif choice == "4":
        break
    else:
        print("Invalid choice")

conn.close()
