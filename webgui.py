import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

#  DATABASE CONNECTION 
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="0007",
        database="webgui"
    )

# ADD STUDENT 
def add_student():
    studentname = e2.get()
    coursename = e3.get()

    try:
        fee = float(e4.get())
    except ValueError:
        messagebox.showerror("Input Error", "Fee must be a number")
        return

    if not studentname or not coursename:
        messagebox.showerror("Input Error", "All fields must be filled")
        return

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO registration (name, course, fee) VALUES (%s,%s,%s)",
            (studentname, coursename, fee)
        )
        conn.commit()

        messagebox.showinfo("Success", "Student added successfully")

        clear_entries()
        load_students()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", err)
    finally:
        if conn:
            conn.close()

# UPDATE STUDENT
def update_student():
    studentid = e1.get()
    if not studentid:
        messagebox.showerror("Selection Error", "Select a student first")
        return

    studentname = e2.get()
    coursename = e3.get()

    try:
        fee = float(e4.get())
    except ValueError:
        messagebox.showerror("Input Error", "Fee must be a number")
        return

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE registration SET name=%s, course=%s, fee=%s WHERE id=%s",
            (studentname, coursename, fee, studentid)
        )
        conn.commit()

        messagebox.showinfo("Success", "Student updated successfully")

        clear_entries()
        load_students()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", err)
    finally:
        if conn:
            conn.close()

# DELETE STUDENT
def delete_student():
    studentid = e1.get()
    if not studentid:
        messagebox.showerror("Selection Error", "Select a student first")
        return

    if not messagebox.askyesno("Confirm", "Are you sure to delete?"):
        return

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM registration WHERE id=%s", (studentid,))
        conn.commit()

        messagebox.showinfo("Success", "Student deleted successfully")

        clear_entries()
        load_students()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", err)
    finally:
        if conn:
            conn.close()

# ---------------- LOAD STUDENTS 
def load_students():
    for row in listBox.get_children():
        listBox.delete(row)

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM registration")
        for row in cursor.fetchall():
            listBox.insert("", "end", values=row)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", err)
    finally:
        if conn:
            conn.close()

#  SEARCH 
def search_students():
    keyword = search_entry.get()
    if not keyword:
        messagebox.showerror("Input Error", "Enter name or course to search")
        return

    for row in listBox.get_children():
        listBox.delete(row)

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM registration WHERE name LIKE %s OR course LIKE %s",
            ("%" + keyword + "%", "%" + keyword + "%")
        )

        rows = cursor.fetchall()
        if not rows:
            messagebox.showinfo("Result", "No record found")

        for row in rows:
            listBox.insert("", "end", values=row)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", err)
    finally:
        if conn:
            conn.close()

# CLEAR SEARCH 
def clear_search():
    search_entry.delete(0, tk.END)
    load_students()

#  TREEVIEW SELECT 
def on_treeview_select(event):
    selected = listBox.selection()
    if not selected:
        return

    values = listBox.item(selected[0])["values"]

    e1.config(state="normal")
    e1.delete(0, tk.END)
    e1.insert(0, values[0])
    e1.config(state="readonly")

    e2.delete(0, tk.END)
    e2.insert(0, values[1])

    e3.delete(0, tk.END)
    e3.insert(0, values[2])

    e4.delete(0, tk.END)
    e4.insert(0, values[3])

# CLEAR ENTRIES
def clear_entries():
    e1.config(state="normal")
    e1.delete(0, tk.END)
    e1.config(state="readonly")
    e2.delete(0, tk.END)
    e3.delete(0, tk.END)
    e4.delete(0, tk.END)

# UI 
root = tk.Tk()
root.title("Student Registration System")
root.geometry("750x550")

# Labels
tk.Label(root, text="Student ID").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Name").grid(row=1, column=0, padx=10, pady=5)
tk.Label(root, text="Course").grid(row=2, column=0, padx=10, pady=5)
tk.Label(root, text="Fee").grid(row=3, column=0, padx=10, pady=5)

# Entries
e1 = tk.Entry(root, state="readonly")
e1.grid(row=0, column=1, padx=10, pady=5)

e2 = tk.Entry(root)
e2.grid(row=1, column=1, padx=10, pady=5)

e3 = tk.Entry(root)
e3.grid(row=2, column=1, padx=10, pady=5)

e4 = tk.Entry(root)
e4.grid(row=3, column=1, padx=10, pady=5)

# Buttons
tk.Button(root, text="Add", width=12, command=add_student).grid(row=4, column=0, pady=10)
tk.Button(root, text="Update", width=12, command=update_student).grid(row=4, column=1)
tk.Button(root, text="Delete", width=12, command=delete_student).grid(row=4, column=2)

# Search
tk.Label(root, text="Search (Name / Course)").grid(row=5, column=0, pady=5)
search_entry = tk.Entry(root)
search_entry.grid(row=5, column=1, pady=5)
tk.Button(root, text="Search", command=search_students).grid(row=5, column=2)
tk.Button(root, text="Clear", command=clear_search).grid(row=5, column=3)

# Table
cols = ("id", "name", "course", "fee")
listBox = ttk.Treeview(root, columns=cols, show="headings")
listBox.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

for col in cols:
    listBox.heading(col, text=col)
    listBox.column(col, width=170)

listBox.bind("<ButtonRelease-1>", on_treeview_select)

# Load data
load_students()

root.mainloop()
