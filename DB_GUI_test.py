import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import pymysql
import query as q

# from dotenv import load_dotenv
import os

# load_dotenv()  # This loads the environment variables from .env file into the environment

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


# def connect_to_db():
#     dbname = "dbproj"
#     try:
#         cn = pymysql.connect(
#             host='localhost',
#             user='root',
#             password='Thepasswordispassword1!',
#             client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS,
#             autocommit=True
#         )
#         print("Connection successful!")
#     except pymysql.Error as e:
#         print(f"Error connecting to MySQL: {e}")


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


# def display_players():
#     records = fetch_players()
#     for i in tree.get_children():
#         tree.delete(i)
#     for (id, name, rating) in records:
#         tree.insert("", "end", values=(id, name, rating))
#
#
# def add_player():
#     id = entry_id.get()
#     name = entry_name.get()
#     rating = entry_rating.get()
#     connection = connect_to_db()
#     if connection:
#         cursor = connection.cursor()
#         try:
#             cursor.execute("INSERT INTO Player (ID, Name, Rating) VALUES (%s, %s, %s)", (id, name, rating))
#             connection.commit()
#             display_players()
#             messagebox.showinfo("Success", "Player added successfully")
#         except Error as e:
#             messagebox.showerror("Error adding player", str(e))
#         finally:
#             cursor.close()
#             connection.close()


# gui code
# app = tk.Tk()
# app.title("Database Interaction")
# app.geometry("1920x1080")
#
# frame = ttk.Frame(app, padding=10)
# frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
#
# # info display
# tree = ttk.Treeview(frame, columns=("ID", "Name", "Rating"), show="headings")
# tree.heading("ID", text="ID")
# tree.heading("Name", text="Name")
# tree.heading("Rating", text="Rating")
# tree.grid(row=0, column=0, columnspan=4)
#
# ttk.Button(frame, text="Refresh", command=display_players).grid(row=1, column=0)
#
# ttk.Label(frame, text="ID").grid(row=2, column=0)
# ttk.Label(frame, text="Name").grid(row=2, column=1)
# ttk.Label(frame, text="Rating").grid(row=2, column=2)
#
# entry_id = ttk.Entry(frame)
# entry_id.grid(row=3, column=0)
# entry_name = ttk.Entry(frame)
# entry_name.grid(row=3, column=1)
# entry_rating = ttk.Entry(frame)
# entry_rating.grid(row=3, column=2)
#
# ttk.Button(frame, text="Add Player", command=add_player).grid(row=3, column=3)
#
# app.mainloop()

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Create a container to hold all the pages
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.cursor, self.connection = q.connect_to_db()

        # Dictionary to hold references to all pages
        self.pages = {}

        # GUI creation

        # Create and add pages
        for i, Page in enumerate([Degree]):
            page = Page(self.container, self)
            self.pages[i] = page
            page.grid(row=1, column=0, sticky="nsew")

        self.header()
        self.show_page(0)

    def show_page(self, page):
        # Raise the requested page to the top
        selected_page = self.pages[page]
        selected_page.tkraise()

    def header(self):
        header_frame = tk.Frame(self)  # Create a frame to hold the header buttons
        header_frame.pack(side="top", fill="x")

        for key, page in self.pages.items():
            button = tk.Button(self, text=page.name, command=lambda num=key: self.show_page(num))
            button.pack(side="left")


class Degree(tk.Frame):
    def __init__(self, parent, controller: App, name="Degree"):
        cr = controller.cursor

        tk.Frame.__init__(self, parent)
        self.name = name
        label = tk.Label(self, text=name)
        label.grid(row=0, column=0, columnspan=4)

        # info display
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Level"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Level", text="Level")
        self.tree.grid(row=1, column=0, columnspan=4)

        ttk.Button(self, text="Refresh", command=lambda: displayAll(self.tree, cr, self.name)).grid(row=2, column=0)
        ttk.Button(self, text="Clear", command=lambda: clearAll(self.tree, cr, self.name)).grid(row=2, column=3)

        ttk.Label(self, text="Name").grid(row=3, column=1)
        ttk.Label(self, text="Level").grid(row=3, column=2)

        self.entry_name = ttk.Entry(self)
        self.entry_name.grid(row=4, column=1)
        self.entry_level = ttk.Entry(self)
        self.entry_level.grid(row=4, column=2)

        tk.Button(self, text="Add Degree",
                  command=lambda: (
                      q.enterDegree(cr, (self.entry_name.get(), self.entry_level.get())),
                      displayAll(self.tree, cr, self.name))
                  ).grid(row=4, column=3)


class Course(tk.Frame):
    def __init__(self, parent, controller: App, name="Course"):
        cr = controller.cursor

        tk.Frame.__init__(self, parent)
        self.name = name
        label = tk.Label(self, text=name)
        label.grid(row=0, column=0, columnspan=4)

        # info display
        self.tree = ttk.Treeview(self, columns=("course_num", "course_name"), show="headings")
        self.tree.heading("course_num", text="Number")
        self.tree.heading("course_name", text="Name")
        self.tree.grid(row=1, column=0, columnspan=4)

        ttk.Button(self, text="Refresh", command=lambda: displayAll(self.tree, cr, self.name)).grid(row=2, column=0)
        ttk.Button(self, text="Clear", command=lambda: clearAll(self.tree, cr, self.name)).grid(row=2, column=3)

        ttk.Label(self, text="Number").grid(row=3, column=1)
        ttk.Label(self, text="Name").grid(row=3, column=2)

        self.entry_name = ttk.Entry(self)
        self.entry_name.grid(row=4, column=1)
        self.entry_level = ttk.Entry(self)
        self.entry_level.grid(row=4, column=2)

        tk.Button(self, text="Add Degree",
                  command=lambda: (
                      q.enterDegree(cr, (self.entry_name.get(), self.entry_level.get())),
                      displayAll(self.tree, cr, self.name))
                  ).grid(row=4, column=3)


# Helper functions
def displayAll(tree, cr, name):
    # Clear existing items from the treeview
    for item in tree.get_children():
        tree.delete(item)

    # Fetch degrees from the database
    degrees = q.getTable(cr, name)
    print(degrees)

    # Insert degrees into the treeview
    for degree in degrees:
        tree.insert("", "end", values=degree)


def clearAll(tree, cr, name):
    # Clear existing items from the treeview
    for item in tree.get_children():
        tree.delete(item)

    q.clearTable(cr, name)

    # Fetch degrees from the database
    degrees = q.getTable(cr, name)
    print(degrees)

    # Insert degrees into the treeview
    for degree in degrees:
        tree.insert("", "end", values=degree)


# class Page2(tk.Frame):
#     def __init__(self, parent, controller: SampleApp):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Page 2")
#         label.pack(pady=10, padx=10)
#
#
# class Page3(tk.Frame):
#     def __init__(self, parent, controller: SampleApp):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Page 3")
#         label.grid(row=0, column=0, columnspan=4)
#
#         # info display
#         self.tree = ttk.Treeview(self, columns=("ID", "Name", "Rating"), show="headings")
#         self.tree.heading("ID", text="ID")
#         self.tree.heading("Name", text="Name")
#         self.tree.heading("Rating", text="Rating")
#         self.tree.grid(row=1, column=0, columnspan=4)
#
#         ttk.Button(self, text="Refresh", command=display_players).grid(row=2, column=0)
#
#         ttk.Label(self, text="ID").grid(row=3, column=0)
#         ttk.Label(self, text="Name").grid(row=3, column=1)
#         ttk.Label(self, text="Rating").grid(row=3, column=2)
#
#         self.entry_id = ttk.Entry(self)
#         self.entry_id.grid(row=4, column=0)
#         self.entry_name = ttk.Entry(self)
#         self.entry_name.grid(row=4, column=1)
#         self.entry_rating = ttk.Entry(self)
#         self.entry_rating.grid(row=4, column=2)
#
#         ttk.Button(self, text="Add Player", command=q.enterDegree(parent)).grid(row=4, column=3)

if __name__ == "__main__":
    app = App()
    app.mainloop()
