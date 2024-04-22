import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

#from dotenv import load_dotenv
import os

#load_dotenv()  # This loads the environment variables from .env file into the environment

# Now you can use the environment variables
db_password = os.getenv('DB_PASSWORD')

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=db_password,
            database='hw1DB'
        )
        return connection
    except Error as e:
        messagebox.showerror("Connection Error", str(e))
        return None

def fetch_players():
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT ID, Name, Rating FROM Player")
            records = cursor.fetchall()
            return records
        except Error as e:
            messagebox.showerror("Error fetching players", str(e))
        finally:
            cursor.close()
            connection.close()
    return []

def display_players():
    records = fetch_players()
    for i in tree.get_children():
        tree.delete(i)
    for (id, name, rating) in records:
        tree.insert("", "end", values=(id, name, rating))

def add_player():
    id = entry_id.get()
    name = entry_name.get()
    rating = entry_rating.get()
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO Player (ID, Name, Rating) VALUES (%s, %s, %s)", (id, name, rating))
            connection.commit()
            display_players()
            messagebox.showinfo("Success", "Player added successfully")
        except Error as e:
            messagebox.showerror("Error adding player", str(e))
        finally:
            cursor.close()
            connection.close()

# gui code
app = tk.Tk()
app.title("Database Interaction")
app.geometry("400x300")

frame = ttk.Frame(app, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

tree = ttk.Treeview(frame, columns=("ID", "Name", "Rating"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Rating", text="Rating")
tree.grid(row=0, column=0, columnspan=4)

ttk.Button(frame, text="Refresh", command=display_players).grid(row=1, column=0)
ttk.Label(frame, text="ID").grid(row=2, column=0)
ttk.Label(frame, text="Name").grid(row=2, column=1)
ttk.Label(frame, text="Rating").grid(row=2, column=2)

entry_id = ttk.Entry(frame)
entry_id.grid(row=3, column=0)
entry_name = ttk.Entry(frame)
entry_name.grid(row=3, column=1)
entry_rating = ttk.Entry(frame)
entry_rating.grid(row=3, column=2)

ttk.Button(frame, text="Add Player", command=add_player).grid(row=3, column=3)

app.mainloop()
