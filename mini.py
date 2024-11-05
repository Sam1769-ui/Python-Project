import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# Function to connect to the database
def connect_db():
    return sqlite3.connect('student_database.db')

# Function to create the database and the table
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS students')  # Drop the table if it exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        uid INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        phone TEXT,
        age INTEGER,
        grade TEXT,
        course TEXT
    )
    ''')
    conn.commit()
    conn.close()

create_table()

# Function to add a student
def add_student():
    uid = uid_entry.get()
    name = name_entry.get()
    phone = phone_entry.get()
    age = age_entry.get()
    grade = grade_combobox.get()
    course = course_entry.get()

    if not uid.isdigit() or not name or not phone.isdigit() or not age.isdigit() or not grade or not course:
        messagebox.showwarning("Input Error", "Please fill in all fields with valid data")
        return

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students (uid, name, phone, age, grade, course) VALUES (?, ?, ?, ?, ?, ?)", 
                       (int(uid), name, phone, int(age), grade, course))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully")
    except sqlite3.IntegrityError:
        messagebox.showwarning("Input Error", "Student ID already exists")
    finally:
        conn.close()
        clear_fields()
        view_students()

# Function to view all students
def view_students():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()
    conn.close()
    
    result_area.delete('1.0', tk.END)
    for record in records:
        result_area.insert(tk.END, f"ID: {record[0]}, Name: {record[1]}, Phone: {record[2]}, Age: {record[3]}, Grade: {record[4]}, Course: {record[5]}\n")

# Function to update a student record
def update_student():
    uid_to_update = simpledialog.askinteger("Update Student", "Enter Student ID to update:")
    if uid_to_update is None:
        return

    name = name_entry.get()
    phone = phone_entry.get()
    age = age_entry.get()
    grade = grade_combobox.get()
    course = course_entry.get()
    
    if not name or not phone.isdigit() or not age.isdigit() or not grade or not course:
        messagebox.showwarning("Input Error", "Please fill in all fields with valid data")
        return
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET name=?, phone=?, age=?, grade=?, course=? WHERE uid=?", 
                   (name, phone, int(age), grade, course, uid_to_update))
    conn.commit()
    if cursor.rowcount == 0:
        messagebox.showwarning("Update Error", "No student found with that ID")
    else:
        messagebox.showinfo("Success", "Student updated successfully")
    conn.close()
    clear_fields()
    view_students()

# Function to delete a student record
def delete_student():
    uid_to_delete = simpledialog.askinteger("Delete Student", "Enter Student ID to delete:")
    if uid_to_delete is None:
        return
    
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?"):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE uid=?", (uid_to_delete,))
        conn.commit()
        if cursor.rowcount == 0:
            messagebox.showwarning("Delete Error", "No student found with that ID")
        else:
            messagebox.showinfo("Success", "Student deleted successfully")
        conn.close()
        view_students()

# Function to search for a student by name
def search_student():
    name_to_search = simpledialog.askstring("Search Student", "Enter student name to search:")
    if name_to_search is None:
        return
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + name_to_search + '%',))
    records = cursor.fetchall()
    conn.close()
    
    result_area.delete('1.0', tk.END)
    if records:
        for record in records:
            result_area.insert(tk.END, f"ID: {record[0]}, Name: {record[1]}, Phone: {record[2]}, Age: {record[3]}, Grade: {record[4]}, Course: {record[5]}\n")
    else:
        result_area.insert(tk.END, "No records found")

# Function to clear input fields
def clear_fields():
    uid_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    grade_combobox.set('')
    course_entry.delete(0, tk.END)

# Set up the main application window
app = tk.Tk()
app.title("Student Database")
app.geometry("600x400")
app.configure(bg="#2C3E50")  # Dark blue background

# Create a frame for input fields
input_frame = tk.Frame(app, bg="#34495E")
input_frame.pack(pady=10)

# Create input fields with improved colors
tk.Label(input_frame, text="ID (UID)", bg="#34495E", fg="#ECF0F1").grid(row=0, column=0, padx=5, pady=5)
uid_entry = tk.Entry(input_frame, bg="#ECF0F1")
uid_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Name", bg="#34495E", fg="#ECF0F1").grid(row=1, column=0, padx=5, pady=5)
name_entry = tk.Entry(input_frame, bg="#ECF0F1")
name_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Phone", bg="#34495E", fg="#ECF0F1").grid(row=2, column=0, padx=5, pady=5)
phone_entry = tk.Entry(input_frame, bg="#ECF0F1")
phone_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Age", bg="#34495E", fg="#ECF0F1").grid(row=3, column=0, padx=5, pady=5)
age_entry = tk.Entry(input_frame, bg="#ECF0F1")
age_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Grade", bg="#34495E", fg="#ECF0F1").grid(row=4, column=0, padx=5, pady=5)
grade_combobox = ttk.Combobox(input_frame, values=["A", "B", "C", "D", "F"], state="readonly")
grade_combobox.grid(row=4, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Course", bg="#34495E", fg="#ECF0F1").grid(row=5, column=0, padx=5, pady=5)
course_entry = tk.Entry(input_frame, bg="#ECF0F1")
course_entry.grid(row=5, column=1, padx=5, pady=5)

# Create buttons with a more vibrant color
button_frame = tk.Frame(app, bg="#34495E")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Student", command=add_student, bg="#27AE60", fg="#FFFFFF").grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Update Student", command=update_student, bg="#2980B9", fg="#FFFFFF").grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Delete Student", command=delete_student, bg="#C0392B", fg="#FFFFFF").grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Search Student", command=search_student, bg="#F39C12", fg="#FFFFFF").grid(row=0, column=3, padx=5)
tk.Button(button_frame, text="View Students", command=view_students, bg="#8E44AD", fg="#FFFFFF").grid(row=0, column=4, padx=5)

# Area to display student records
result_area = tk.Text(app, width=70, height=10, bg="#ECF0F1", fg="#2C3E50")
result_area.pack(pady=10)

# Call this function to load existing students into the text area when the app starts
view_students()

app.mainloop()