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


# def connect_to_db():
#     try:
#         connection = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password=db_password,
#             database='hw1DB'
#         )
#         return connection
#     except Error as e:
#         messagebox.showerror("Connection Error", str(e))
#         return None


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


# def fetch_players():
#     connection = connect_to_db()
#     if connection:
#         cursor = connection.cursor()
#         try:
#             cursor.execute("SELECT ID, Name, Rating FROM Player")
#             records = cursor.fetchall()
#             return records
#         except Error as e:
#             messagebox.showerror("Error fetching players", str(e))
#         finally:
#             cursor.close()
#             connection.close()
#     return []


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
        for i, Page in enumerate([Degree, Course, Objective, DegCourse, Instructor, Section, Evaluation,
                                  DegreeSearch]):
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
        self.tree = ttk.Treeview(self, columns=("Name", "Level"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Level", text="Level")
        self.tree.grid(row=1, column=0, columnspan=4)

        ttk.Button(self, text="Refresh", command=lambda: displayAll(self.tree, cr, self.name)).grid(row=2, column=1)
        ttk.Button(self, text="Clear", command=lambda: clearAll(self.tree, cr, self.name)).grid(row=2, column=2)

        ttk.Label(self, text="Name").grid(row=3, column=1)
        ttk.Label(self, text="Level").grid(row=3, column=2)

        self.entry_name = ttk.Entry(self)
        self.entry_name.grid(row=4, column=1)
        self.entry_level = ttk.Entry(self)
        self.entry_level.grid(row=4, column=2)

        tk.Button(self, text="Add",
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

        ttk.Button(self, text="Refresh", command=lambda: displayAll(self.tree, cr, self.name)).grid(row=2, column=1)
        ttk.Button(self, text="Clear", command=lambda: clearAll(self.tree, cr, self.name)).grid(row=2, column=2)

        ttk.Label(self, text="Number").grid(row=3, column=1)
        ttk.Label(self, text="Name").grid(row=3, column=2)

        self.entry_num = ttk.Entry(self)
        self.entry_num.grid(row=4, column=1)
        self.entry_name = ttk.Entry(self)
        self.entry_name.grid(row=4, column=2)

        tk.Button(self, text="Add",
                  command=lambda: (
                      q.enterCourse(cr, (self.entry_num.get(), self.entry_name.get())),
                      displayAll(self.tree, cr, self.name))
                  ).grid(row=4, column=3)


class Instructor(tk.Frame):
    def __init__(self, parent, controller: App, name="Instructor"):
        cr = controller.cursor

        tk.Frame.__init__(self, parent)
        self.name = name
        label = tk.Label(self, text=name)
        label.grid(row=0, column=0, columnspan=4)

        # info display
        self.tree = ttk.Treeview(self, columns=("instruct_id", "instruct_name"), show="headings")
        self.tree.heading("instruct_id", text="ID")
        self.tree.heading("instruct_name", text="Name")
        self.tree.grid(row=1, column=0, columnspan=4)

        ttk.Button(self, text="Refresh", command=lambda: displayAll(self.tree, cr, self.name)).grid(row=2, column=1)
        ttk.Button(self, text="Clear", command=lambda: clearAll(self.tree, cr, self.name)).grid(row=2, column=2)

        ttk.Label(self, text="ID").grid(row=3, column=1)
        ttk.Label(self, text="Name").grid(row=3, column=2)

        self.entry_id = ttk.Entry(self)
        self.entry_id.grid(row=4, column=1)
        self.entry_number = ttk.Entry(self)
        self.entry_number.grid(row=4, column=2)

        tk.Button(self, text="Add",
                  command=lambda: (
                      q.enterInstructor(cr, (self.entry_id.get(), self.entry_number.get())),
                      displayAll(self.tree, cr, self.name))
                  ).grid(row=4, column=3)


class Evaluation(tk.Frame):
    def __init__(self, parent, controller: App, name="Evaluation"):
        cr = controller.cursor

        tk.Frame.__init__(self, parent)
        self.name = name
        label = tk.Label(self, text=name)
        label.grid(row=0, column=0, columnspan=6)

        ttk.Label(self, text="Degree Name", anchor="center").grid(row=1, column=0)
        self.entry_name = ttk.Entry(self)
        self.entry_name.grid(row=1, column=1)
        ttk.Label(self, text="Degree Level", anchor="center").grid(row=1, column=2)
        self.entry_level = ttk.Entry(self)
        self.entry_level.grid(row=1, column=3)
        ttk.Label(self, text="Semester Year", anchor="center").grid(row=1, column=4)
        self.entry_year = ttk.Entry(self)
        self.entry_year.grid(row=1, column=5)
        ttk.Label(self, text="Semester Term", anchor="center").grid(row=1, column=6)
        self.entry_term = ttk.Entry(self)
        self.entry_term.grid(row=1, column=7)
        ttk.Label(self, text="Instructor ID", anchor="center").grid(row=1, column=8)
        self.entry_id = ttk.Entry(self)
        self.entry_id.grid(row=1, column=9)

        info = (self.entry_id.get(), self.entry_year.get(),
                self.entry_term.get())

        sections = q.fromInstructorGetSections(cr, info)
        self.tree = ttk.Treeview(self, columns=(
            ""), show="headings")

        self.tree = ttk.Treeview(self, columns=(
            "sect_id", "course_num"), show="headings")
        populateTree(self.tree, sections)

        # info display
        self.tree = ttk.Treeview(self, columns=(
            "sem_year", "sem_term", "sect_id", "eval_obj", "eval_description", "obj_code", "course_num", "instruct_id",
            "num_A", "num_B", "num_C", "num_F"), show="headings")
        self.tree.heading("sem_year", text="Semester Year")
        self.tree.heading("sem_term", text="Semester Term")
        self.tree.heading("sect_id", text="Section ID")
        self.tree.heading("eval_obj", text="Evaluation Objective")
        self.tree.heading("eval_description", text="Evaluation Description")
        self.tree.heading("obj_code", text="Object Code")
        self.tree.heading("course_num", text="Course Number")
        self.tree.heading("instruct_id", text="Instructor ID")
        self.tree.heading("num_A", text="Number of A Grades")
        self.tree.heading("num_B", text="Number of B Grades")
        self.tree.heading("num_C", text="Number of C Grades")
        self.tree.heading("num_F", text="Number of F Grades")
        self.tree.grid(row=4, column=0, columnspan=6)

        self.tree.grid(row=4, column=0, columnspan=6)

        ttk.Button(self, text="Refresh", command=lambda: displayAll(self.tree, cr, self.name)).grid(row=5, column=0)
        ttk.Button(self, text="Clear", command=lambda: clearAll(self.tree, cr, self.name)).grid(row=5, column=1)

        ttk.Label(self, text="Semester Year").grid(row=6, column=0)
        ttk.Label(self, text="Semester Term").grid(row=6, column=1)
        ttk.Label(self, text="Section ID").grid(row=6, column=2)
        ttk.Label(self, text="Learning Objective").grid(row=6, column=3)
        ttk.Label(self, text="Description").grid(row=6, column=4)
        ttk.Label(self, text="Object Code").grid(row=6, column=5)
        ttk.Label(self, text="Course Number").grid(row=8, column=6)
        ttk.Label(self, text="Instructor ID").grid(row=8, column=7)
        ttk.Label(self, text="Number of As").grid(row=8, column=8)
        ttk.Label(self, text="Number of Bs").grid(row=8, column=9)
        ttk.Label(self, text="Number of Cs").grid(row=8, column=9)
        ttk.Label(self, text="Number of Fs").grid(row=8, column=6)

        # self.entry_sem_year = ttk.Entry(self)
        # self.entry_sem_year.grid(row=4, column=1)
        # self.entry_sem_term = ttk.Entry(self)
        # self.entry_sem_term.grid(row=4, column=2)
        # self.entry_sect_id = ttk.Entry(self)
        # self.entry_sect_id.grid(row=4, column=3)
        # self.entry_eval_obj = ttk.Entry(self)
        # self.entry_eval_obj.grid(row=4, column=4)
        # self.entry_eval_description = ttk.Entry(self)
        # self.entry_eval_description.grid(row=4, column=5)
        # self.entry_obj_code = ttk.Entry(self)
        # self.entry_obj_code.grid(row=4, column=6)
        # self.entry_course_num = ttk.Entry(self)
        # self.entry_course_num.grid(row=6, column=1)
        # self.entry_instruct_id = ttk.Entry(self)
        # self.entry_instruct_id.grid(row=6, column=2)
        # self.entry_num_A = ttk.Entry(self)
        # self.entry_num_A.grid(row=6, column=3)
        # self.entry_num_B = ttk.Entry(self)
        # self.entry_num_B.grid(row=6, column=4)
        # self.entry_num_C = ttk.Entry(self)
        # self.entry_num_C.grid(row=6, column=5)
        # self.entry_num_F = ttk.Entry(self)
        # self.entry_num_F.grid(row=6, column=6)
        #
        # tk.Button(self, text="Add",
        #           command=lambda: (
        #               q.enterEvaluation(cr,
        #                                 (self.entry_sem_year.get(), self.entry_sem_term.get(), self.entry_sect_id.get(),
        #                                  self.entry_eval_obj.get(), self.entry_eval_description.get(),
        #                                  self.entry_obj_code.get(), self.entry_course_num.get(),
        #                                  self.entry_instruct_id.get(), self.entry_num_A.get(),
        #                                  self.entry_num_B.get(), self.entry_num_C.get(), self.entry_num_F.get())),
        #               displayAll(self.tree, cr, self.name))
        #           ).grid(row=2, column=3)


class Section(tk.Frame):
    def __init__(self, parent, controller: App, tableName="Section", name="Section"):
        cr = controller.cursor

        tk.Frame.__init__(self, parent)
        self.tableName = tableName
        self.name = name
        label = tk.Label(self, text=name)
        label.grid(row=0, column=0, columnspan=4)

        # info display
        self.tree = ttk.Treeview(self,
                                 columns=("sect_id", "num_studs", "sem_year", "sem_term", "instruct_id", "course_num"),
                                 show="headings")
        self.tree.heading("sect_id", text="Section ID")
        self.tree.heading("num_studs", text="Number of Students")
        self.tree.heading("sem_year", text="Semester Year")
        self.tree.heading("sem_term", text="Semester Term")
        self.tree.heading("instruct_id", text="Instructor ID")
        self.tree.heading("course_num", text="Course Number")
        self.tree.grid(row=1, column=0, columnspan=4)

        ttk.Button(self, text="Refresh", command=lambda: displayAll(self.tree, cr, self.tableName)).grid(row=2,
                                                                                                         column=1)
        ttk.Button(self, text="Clear", command=lambda: clearAll(self.tree, cr, self.tableName)).grid(row=2, column=2)

        ttk.Label(self, text="ID").grid(row=3, column=1)
        ttk.Label(self, text="Number").grid(row=3, column=2)

        self.entry_id = ttk.Entry(self)
        self.entry_id.grid(row=4, column=1)
        self.entry_number = ttk.Entry(self)
        self.entry_number.grid(row=4, column=2)

        ttk.Label(self, text="ID").grid(row=3, column=1)
        ttk.Label(self, text="Number of Students").grid(row=3, column=2)
        ttk.Label(self, text="Semester Year").grid(row=3, column=3)
        ttk.Label(self, text="Semester Term").grid(row=3, column=4)
        ttk.Label(self, text="Instructor ID").grid(row=3, column=5)
        ttk.Label(self, text="Course Number").grid(row=3, column=6)

        self.entry_id = ttk.Entry(self)
        self.entry_id.grid(row=4, column=1)
        self.entry_number = ttk.Entry(self)
        self.entry_number.grid(row=4, column=2)
        self.entry_sem_year = ttk.Entry(self)
        self.entry_sem_year.grid(row=4, column=3)
        self.entry_sem_term = ttk.Entry(self)
        self.entry_sem_term.grid(row=4, column=4)
        self.entry_instruct_id = ttk.Entry(self)
        self.entry_instruct_id.grid(row=4, column=5)
        self.entry_course_num = ttk.Entry(self)
        self.entry_course_num.grid(row=4, column=6)

        tk.Button(self, text="Add",
                  command=lambda: (
                      q.enterSection(cr, (self.entry_id.get(), self.entry_number.get(), self.entry_sem_year.get(),
                                          self.entry_sem_term.get(), self.entry_instruct_id.get(),
                                          self.entry_course_num.get())),
                      displayAll(self.tree, cr, self.tableName))
                  ).grid(row=4, column=7)


class Objective(tk.Frame):
    def __init__(self, parent, controller: App, tableName="learning_obj", name="Learning Objective"):
        cr = controller.cursor

        tk.Frame.__init__(self, parent)
        self.tableName = tableName
        self.name = name
        label = tk.Label(self, text=name)
        label.grid(row=0, column=0, columnspan=3)

        # info display
        self.tree = ttk.Treeview(self, columns=("obj_code", "lo_title", "description"), show="headings")
        self.tree.heading("obj_code", text="Object Code")
        self.tree.heading("lo_title", text="Objective Title")
        self.tree.heading("description", text="Description")
        self.tree.grid(row=1, column=0, columnspan=3)

        ttk.Button(self, text="Refresh", command=lambda: displayAll(self.tree, cr, self.tableName)).grid(row=2,
                                                                                                         column=0)
        ttk.Button(self, text="Clear", command=lambda: clearAll(self.tree, cr, self.tableName)).grid(row=2, column=1)

        ttk.Label(self, text="Title").grid(row=3, column=0)
        ttk.Label(self, text="Description").grid(row=3, column=1)

        self.entry_title = ttk.Entry(self)
        self.entry_title.grid(row=4, column=0)
        self.entry_description = ttk.Entry(self)
        self.entry_description.grid(row=4, column=1)

        tk.Button(self, text="Add",
                  command=lambda: (
                      q.enterObjective(cr, (self.entry_title.get(), self.entry_description.get())),
                      displayAll(self.tree, cr, self.tableName))
                  ).grid(row=4, column=2)


class DegCourse(tk.Frame):
    def __init__(self, parent, controller: App, tableName="degree_course", name="DegCourse"):
        cr = controller.cursor

        tk.Frame.__init__(self, parent)
        self.tableName = tableName
        self.name = name
        label = tk.Label(self, text=name)
        label.grid(row=0, column=0, columnspan=3)

        # info display
        self.tree = ttk.Treeview(self, columns=("name", "level", "course_code", "is_core"), show="headings")
        self.tree.heading("name", text="Name")
        self.tree.heading("level", text="Level")
        self.tree.heading("course_code", text="Course Code")
        self.tree.heading("is_core", text="Is Core")
        self.tree.grid(row=1, column=0, columnspan=3)

        ttk.Button(self, text="Refresh", command=lambda: displayAll(self.tree, cr, self.tableName)).grid(row=2,
                                                                                                         column=0)
        ttk.Button(self, text="Clear", command=lambda: clearAll(self.tree, cr, self.tableName)).grid(row=2, column=1)

        ttk.Label(self, text="Name").grid(row=3, column=0)
        ttk.Label(self, text="Level").grid(row=3, column=1)
        ttk.Label(self, text="Course Code").grid(row=3, column=2)
        ttk.Label(self, text="Is Core").grid(row=3, column=3)

        self.entry_name = ttk.Entry(self)
        self.entry_name.grid(row=4, column=0)
        self.entry_level = ttk.Entry(self)
        self.entry_level.grid(row=4, column=1)
        self.entry_course_code = ttk.Entry(self)
        self.entry_course_code.grid(row=4, column=2)
        check_var = tk.BooleanVar()
        self.entry_is_core = ttk.Checkbutton(self, variable=check_var)
        self.entry_is_core.grid(row=4, column=3)

        tk.Button(self, text="Add",
                  command=lambda: (
                      q.enterDegCourse(cr, (self.entry_name.get(), self.entry_level.get(), self.entry_course_code.get(),
                                            check_var.get())),
                      displayAll(self.tree, cr, self.tableName))
                  ).grid(row=4, column=4)


class ObjCourse(tk.Frame):
    def __init__(self, parent, controller: App, tableName="obj_course", name="Objective Course"):
        cr = controller.cursor

        tk.Frame.__init__(self, parent)
        self.tableName = tableName
        self.name = name
        label = tk.Label(self, text=name)
        label.grid(row=0, column=0, columnspan=3)

        # info display
        self.tree = ttk.Treeview(self, columns=("course_num", "obj_code"), show="headings")
        self.tree.heading("course_num", text="Course Number")
        self.tree.heading("obj_code", text="Objective Code")
        self.tree.grid(row=1, column=0, columnspan=3)

        ttk.Button(self, text="Refresh", command=lambda: displayAll(self.tree, cr, self.tableName)).grid(row=2,
                                                                                                         column=0)
        ttk.Button(self, text="Clear", command=lambda: clearAll(self.tree, cr, self.tableName)).grid(row=2, column=1)

        ttk.Label(self, text="Course Number").grid(row=3, column=0)
        ttk.Label(self, text="Objective Code").grid(row=3, column=1)

        self.entry_num = ttk.Entry(self)
        self.entry_num.grid(row=4, column=0)
        self.entry_code = ttk.Entry(self)
        self.entry_code.grid(row=4, column=1)

        tk.Button(self, text="Add",
                  command=lambda: (
                      q.enterObjCourse(cr, (self.entry_num.get(), self.entry_code.get(), self.entry_course_code.get(),
                                            self.entry_is_core.get())),
                      displayAll(self.tree, cr, self.tableName))
                  ).grid(row=4, column=4)


# Query
class DegreeSearch(tk.Frame):
    def __init__(self, parent, controller: App, name="Degree Search"):
        cr = controller.cursor

        tk.Frame.__init__(self, parent)
        self.name = name
        label = tk.Label(self, text=name)
        label.grid(row=0, column=0, columnspan=4)

        ttk.Label(self, text="Name", anchor="center").grid(row=1, column=0)
        self.entry_name = ttk.Entry(self)
        self.entry_name.grid(row=1, column=1)
        ttk.Label(self, text="Level", anchor="center").grid(row=1, column=2)
        self.entry_level = ttk.Entry(self)
        self.entry_level.grid(row=1, column=3)

        info = (self.entry_name.get(), self.entry_level.get())

        tk.Button(self, text="Search",
                  command=lambda: (
                      populateTree(self.treeCourse, q.fromDegreeGetCourse(cr, info)),
                      populateTree(self.treeSect, q.fromDegreeGetSects(cr, info))

                  )
                  ).grid(row=1, column=5)

        # info display
        ttk.Label(self, text="Associated Courses", anchor="center").grid(row=2, column=0)
        self.treeCourse = ttk.Treeview(self, columns=("Name", "IsCore"), show="headings")
        self.treeCourse.heading("Name", text="Names")
        self.treeCourse.heading("IsCore", text="IsCore")
        self.treeCourse.grid(row=3, column=0, columnspan=2)

        ttk.Label(self, text="Associated Sections", anchor="center").grid(row=2, column=3)
        self.treeSect = ttk.Treeview(self, columns=("Name", "IsCore"), show="headings")
        self.treeSect.heading("Name", text="Names")
        self.treeSect.heading("IsCore", text="IsCore")
        self.treeSect.grid(row=3, column=3, columnspan=2)

        # ttk.Label(self, text="Associated Objectives", anchor="center").grid(row=2, column=6)
        # self.treeSect = ttk.Treeview(self, columns=("Obj", "IsCore"), show="headings")
        # self.treeSect.heading("Objective", text="Objective")
        # self.treeSect.grid(row=3, column=6, columnspan=2)
        #
        # populateTree(self.treeSect, q.fromDegreeGetObj(cr, info))

        # ttk.Button(self, text="Refresh", command=lambda: displayAll(self.treeCourse, cr, self.name)).grid(row=3, column=1)
        # ttk.Button(self, text="Clear", command=lambda: clearAll(self.treeCourse, cr, self.name)).grid(row=3, column=2)


class CourseSearch(tk.Frame):
    def __init__(self, parent, controller: App, name="Degree Search"):
        cr = controller.cursor

        tk.Frame.__init__(self, parent)
        self.name = name
        label = tk.Label(self, text=name)
        label.grid(row=0, column=0, columnspan=4)

        ttk.Label(self, text="Course Number", anchor="center").grid(row=1, column=0)
        self.entry_name = ttk.Entry(self)
        self.entry_name.grid(row=1, column=1)
        ttk.Label(self, text="Course Name", anchor="center").grid(row=1, column=2)
        self.entry_level = ttk.Entry(self)
        self.entry_level.grid(row=1, column=3)

        info = (self.entry_name.get(), self.entry_level.get())

        tk.Button(self, text="Search",
                  command=lambda: (
                      populateTree(self.treeCourse, q.fromDegreeGetCourse(cr, info)),
                      populateTree(self.treeSect, q.fromDegreeGetSects(cr, info))

                  )
                  ).grid(row=1, column=5)

        # info display
        ttk.Label(self, text="Associated Courses", anchor="center").grid(row=2, column=0)
        self.treeCourse = ttk.Treeview(self, columns=("Name", "IsCore"), show="headings")
        self.treeCourse.heading("Name", text="Names")
        self.treeCourse.heading("IsCore", text="IsCore")
        self.treeCourse.grid(row=3, column=0, columnspan=2)

        ttk.Label(self, text="Associated Sections", anchor="center").grid(row=2, column=3)
        self.treeSect = ttk.Treeview(self, columns=("Name", "IsCore"), show="headings")
        self.treeSect.heading("Name", text="Names")
        self.treeSect.heading("IsCore", text="IsCore")
        self.treeSect.grid(row=3, column=3, columnspan=2)

        # ttk.Label(self, text="Associated Objectives", anchor="center").grid(row=2, column=6)
        # self.treeSect = ttk.Treeview(self, columns=("Obj", "IsCore"), show="headings")
        # self.treeSect.heading("Objective", text="Objective")
        # self.treeSect.grid(row=3, column=6, columnspan=2)
        #
        # populateTree(self.treeSect, q.fromDegreeGetObj(cr, info))

        # ttk.Button(self, text="Refresh", command=lambda: displayAll(self.treeCourse, cr, self.name)).grid(row=3, column=1)
        # ttk.Button(self, text="Clear", command=lambda: clearAll(self.treeCourse, cr, self.name)).grid(row=3, column=2)


def populateTree(tree, values):
    # Clear existing items from the treeview
    for item in tree.get_children():
        tree.delete(item)

    # Insert degrees into the treeview
    for value in values:
        tree.insert("", "end", values=value)


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

def addDummyData(cr):
    q.dropAll(cr)
    q.createTables(cr)
    if cr is None:
        print("Table creation failed.")

    degreeData = [
        ("cs", "PHD"),
        ("eng", "MS"),
        ("art", "BA"),
        ("math", "BS")
    ]

    for degree in degreeData:
        q.enterDegree(cr, degree)

    result = q.getAllDegree(cr)
    print(result)
    print(len(result))

    courseData = [
        ("CS1234", "Intro to Computer Science"),
        ("EN4321", "Creative Writing"),
        ("AR2233", "How to Use a Pencil"),
        ("MA1324", "Math 101: Calculating Quantum Topology")
    ]

    for course in courseData:
        q.enterCourse(cr, course)

    result = q.getTable(cr, "course")
    print(result)
    print(len(result))

    q.close_db(cn)


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
