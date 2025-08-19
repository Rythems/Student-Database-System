import sqlite3
import tkinter as tk
from tkinter import messagebox

# ---------------- DATABASE SETUP ----------------
conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    marks INTEGER NOT NULL
)
""")
conn.commit()

# ---------------- FUNCTIONS ----------------
def add_student():
    roll = entry_roll.get()
    name = entry_name.get()
    marks = entry_marks.get()

    if roll == "" or name == "" or marks == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        cursor.execute("INSERT INTO students (roll, name, marks) VALUES (?, ?, ?)", 
                       (int(roll), name, int(marks)))
        conn.commit()
        messagebox.showinfo("Success", f"Student {name} added!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll number already exists!")
    clear_entries()

def view_students():
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()
    result = "\n".join([f"Roll: {r[0]}, Name: {r[1]}, Marks: {r[2]}" for r in records])
    messagebox.showinfo("All Students", result if result else "No students found!")

def topper():
    cursor.execute("SELECT name, MAX(marks) FROM students")
    record = cursor.fetchone()
    if record and record[0]:
        messagebox.showinfo("Topper", f"Topper: {record[0]} with {record[1]} marks")
    else:
        messagebox.showinfo("Topper", "No data found!")

def average_marks():
    cursor.execute("SELECT AVG(marks) FROM students")
    avg = cursor.fetchone()[0]
    if avg:
        messagebox.showinfo("Average Marks", f"Average Marks: {avg:.2f}")
    else:
        messagebox.showinfo("Average Marks", "No data found!")

def clear_entries():
    entry_roll.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_marks.delete(0, tk.END)

# ---------------- GUI SETUP ----------------
root = tk.Tk()
root.title("Student Database System")

tk.Label(root, text="Roll Number:").grid(row=0, column=0)
entry_roll = tk.Entry(root)
entry_roll.grid(row=0, column=1)

tk.Label(root, text="Name:").grid(row=1, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1)

tk.Label(root, text="Marks:").grid(row=2, column=0)
entry_marks = tk.Entry(root)
entry_marks.grid(row=2, column=1)

tk.Button(root, text="Add Student", command=add_student).grid(row=3, column=0, pady=5)
tk.Button(root, text="View Students", command=view_students).grid(row=3, column=1, pady=5)
tk.Button(root, text="Find Topper", command=topper).grid(row=4, column=0, pady=5)
tk.Button(root, text="Average Marks", command=average_marks).grid(row=4, column=1, pady=5)

root.mainloop()
