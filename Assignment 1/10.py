# Q10 - Tkinter Assignment Tracker

import tkinter as tk
from tkinter import ttk, messagebox
import json
import csv
import os


DATA_FILE = "assignments.json"

records = []


# -----------------------------
# Load existing data
# -----------------------------

def load_data():

    global records

    if os.path.exists(DATA_FILE):

        try:

            with open(DATA_FILE, "r") as file:
                records = json.load(file)

        except:
            records = []


# -----------------------------
# Save data
# -----------------------------

def save_data():

    with open(DATA_FILE, "w") as file:
        json.dump(records, file, indent=4)


# -----------------------------
# Add student
# -----------------------------

def add_student():

    enrollment = enrollment_entry.get().strip()
    name = name_entry.get().strip()

    if not enrollment or not name:

        messagebox.showerror(
            "Error",
            "Enter enrollment and name"
        )

        return

    # Check whether student already exists
    for record in records:

        if (
            record["enrollment"] == enrollment
            and record["name"] == name
        ):

            messagebox.showwarning(
                "Already Exists",
                "Student already exists"
            )

            return

    records.append({
        "enrollment": enrollment,
        "name": name,
        "assignment": "",
        "status": "Pending",
        "marks": "",
        "remarks": ""
    })

    save_data()

    enrollment_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)

    refresh_table()

    messagebox.showinfo(
        "Success",
        "Student added"
    )


# -----------------------------
# Add / Update Assignment
# -----------------------------

def add_assignment():

    enrollment = enrollment_entry.get().strip()
    assignment = assignment_entry.get().strip()
    marks = marks_entry.get().strip()
    remarks = remarks_entry.get().strip()

    if not enrollment or not assignment:

        messagebox.showerror(
            "Error",
            "Enter enrollment and assignment"
        )

        return

    try:

        if marks:
            marks_value = float(marks)

            if marks_value < 0 or marks_value > 100:
                raise ValueError

        else:
            marks_value = ""

    except ValueError:

        messagebox.showerror(
            "Error",
            "Marks must be between 0 and 100"
        )

        return

    found = False

    for record in records:

        if record["enrollment"] == enrollment:

            record["assignment"] = assignment
            record["marks"] = marks_value
            record["remarks"] = remarks

            if marks:
                record["status"] = "Completed"
            else:
                record["status"] = "Pending"

            found = True
            break

    if not found:

        messagebox.showerror(
            "Error",
            "Student not found"
        )

        return

    save_data()
    refresh_table()

    messagebox.showinfo(
        "Success",
        "Assignment updated"
    )


# -----------------------------
# Filter records
# -----------------------------

def filter_records():

    selected = filter_box.get()

    for item in table.get_children():
        table.delete(item)

    for record in records:

        if selected == "All":

            show = True

        elif selected == record["status"]:

            show = True

        else:

            show = False

        if show:

            table.insert(
                "",
                tk.END,
                values=(
                    record["enrollment"],
                    record["name"],
                    record["assignment"],
                    record["status"],
                    record["marks"],
                    record["remarks"]
                )
            )


# -----------------------------
# Refresh table
# -----------------------------

def refresh_table():

    filter_records()


# -----------------------------
# Export CSV
# -----------------------------

def export_csv():

    filename = "assignment_report.csv"

    with open(
        filename,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Enrollment",
            "Name",
            "Assignment",
            "Status",
            "Marks",
            "Remarks"
        ])

        for record in records:

            writer.writerow([
                record["enrollment"],
                record["name"],
                record["assignment"],
                record["status"],
                record["marks"],
                record["remarks"]
            ])

    messagebox.showinfo(
        "Export Complete",
        f"Report saved as {filename}"
    )


# -----------------------------
# GUI
# -----------------------------

root = tk.Tk()

root.title("Assignment Tracker")
root.geometry("900x600")


title = tk.Label(
    root,
    text="Student Assignment Tracker",
    font=("Arial", 20, "bold")
)

title.pack(pady=10)


form = tk.Frame(root)
form.pack(pady=10)


tk.Label(
    form,
    text="Enrollment"
).grid(row=0, column=0, padx=5, pady=5)

enrollment_entry = tk.Entry(form)
enrollment_entry.grid(
    row=0,
    column=1,
    padx=5
)


tk.Label(
    form,
    text="Name"
).grid(row=0, column=2, padx=5)

name_entry = tk.Entry(form)
name_entry.grid(
    row=0,
    column=3,
    padx=5
)


tk.Label(
    form,
    text="Assignment"
).grid(row=1, column=0, padx=5)

assignment_entry = tk.Entry(form)
assignment_entry.grid(
    row=1,
    column=1,
    padx=5
)


tk.Label(
    form,
    text="Marks"
).grid(row=1, column=2, padx=5)

marks_entry = tk.Entry(form)
marks_entry.grid(
    row=1,
    column=3,
    padx=5
)


tk.Label(
    form,
    text="Remarks"
).grid(row=2, column=0, padx=5)

remarks_entry = tk.Entry(form)
remarks_entry.grid(
    row=2,
    column=1,
    padx=5
)


tk.Button(
    form,
    text="Add Student",
    command=add_student
).grid(
    row=3,
    column=0,
    pady=10
)


tk.Button(
    form,
    text="Add / Update Assignment",
    command=add_assignment
).grid(
    row=3,
    column=1,
    pady=10
)


tk.Button(
    form,
    text="Export CSV",
    command=export_csv
).grid(
    row=3,
    column=2,
    pady=10
)


tk.Label(
    form,
    text="Filter"
).grid(
    row=4,
    column=0
)


filter_box = ttk.Combobox(
    form,
    values=[
        "All",
        "Pending",
        "Completed"
    ],
    state="readonly"
)

filter_box.set("All")

filter_box.grid(
    row=4,
    column=1
)

filter_box.bind(
    "<<ComboboxSelected>>",
    lambda event: filter_records()
)


# -----------------------------
# Table
# -----------------------------

columns = (
    "Enrollment",
    "Name",
    "Assignment",
    "Status",
    "Marks",
    "Remarks"
)

table = ttk.Treeview(
    root,
    columns=columns,
    show="headings"
)

for column in columns:

    table.heading(
        column,
        text=column
    )

    table.column(
        column,
        width=130
    )

table.pack(
    fill=tk.BOTH,
    expand=True,
    padx=10,
    pady=10
)


load_data()
refresh_table()

root.mainloop()