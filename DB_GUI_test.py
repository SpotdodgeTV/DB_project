import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

def create_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',       # or your host, e.g., '127.0.0.1'
            user='your_username',   # your MySQL username
            password='your_password', # your MySQL password
            database='your_database'  # your database name
        )
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                age INT
            )
        ''')
        conn.commit()
    except Error as e:
        messagebox.showerror("Error", str(e))
    finally:
        if conn.is_connected():
            conn.close()

def add_record(name, age):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='your_database'
        )
        c = conn.cursor()
        c.execute('INSERT INTO records (name, age) VALUES (%s, %s)', (name, age))
        conn.commit()
    except Error as e:
        messagebox.showerror("Error", str(e))
    finally:
        if conn.is_connected():
            conn.close()
        view_records()

def view_records():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='your_database'
        )
        c = conn.cursor()
        c.execute('SELECT * FROM records')
        records = c.fetchall()
        listbox.delete(0, tk.END)
        for record in records:
            listbox.insert(tk.END, record)
    except Error as e:
        messagebox.showerror("Error", str(e))
    finally:
        if conn.is_connected():
            conn.close()

def delete_record():
    try:
        selected_item = listbox.curselection()[0]
        id_to_delete = listbox.get(selected_item)[0]
        conn = mysql.connector.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='your_database'
        )
        c = conn.cursor()
        c.execute('DELETE FROM records WHERE id=%s', (id_to_delete,))
        conn.commit()
    except Error as e:
        messagebox.showerror("Error", str(e))
    finally:
        if conn.is_connected():
            conn.close()
        view_records()

# GUI setup
root = tk.Tk()
root.title("Database Interface")
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1)
entry_age = tk.Entry(root)
entry_age.grid(row=1, column=1)
add_button = tk.Button(root, text="Add Record", command=lambda: add_record(entry_name.get(), entry_age.get()))
add_button.grid(row=2, column=1)
view_button = tk.Button(root, text="View Records", command=view_records)
view_button.grid(row=3, column=1)
delete_button = tk.Button(root, text="Delete Selected", command=delete_record)
delete_button.grid(row=4, column=1)
listbox = tk.Listbox(root)
listbox.grid(row=0, column=0, rowspan=4)
create_db()
root.mainloop()
