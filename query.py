import pymysql
import pymysql.cursors
import os
from dotenv import load_dotenv
# import nicoPlayground

load_dotenv()
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')


# data manipulation commands
def createTables(c):
    create_table_queries = [
        """
        CREATE TABLE IF NOT EXISTS learning_obj (
            obj_code INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            lo_title VARCHAR(50) NOT NULL UNIQUE,
            description VARCHAR(300)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS degree (
            deg_name VARCHAR(50) NOT NULL,
            deg_level VARCHAR(10) NOT NULL,
            PRIMARY KEY (deg_name, deg_level)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS course (
            course_num VARCHAR(8) NOT NULL PRIMARY KEY,
            course_name VARCHAR(50) NOT NULL UNIQUE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS degree_course (
            deg_name VARCHAR(50) NOT NULL,
            deg_level VARCHAR(8) NOT NULL,
            course_num VARCHAR(8) NOT NULL,
            is_core BOOL,
            FOREIGN KEY (course_num) REFERENCES course(course_num),
            FOREIGN KEY (deg_name, deg_level) REFERENCES degree(deg_name, deg_level),
            PRIMARY KEY (course_num, deg_name, deg_level)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS obj_course (
            obj_code INT UNSIGNED NOT NULL,
            course_num VARCHAR(8) NOT NULL,
            PRIMARY KEY (obj_code, course_num),
            FOREIGN KEY (course_num) REFERENCES course(course_num),
            FOREIGN KEY (obj_code) REFERENCES learning_obj(obj_code)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS semester (
            year INT UNSIGNED NOT NULL,
            term VARCHAR(6) NOT NULL,
            PRIMARY KEY (year, term)  -- Added primary key constraint
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS instructor (
            instruct_id INT UNSIGNED NOT NULL PRIMARY KEY,
            instruct_name VARCHAR(50) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS section (
            sect_id INT AUTO_INCREMENT,
            num_studs INT UNSIGNED,
            sem_year INT UNSIGNED NOT NULL,
            sem_term VARCHAR(6) NOT NULL,
            instruct_id INT UNSIGNED NOT NULL,
            course_num VARCHAR(8) NOT NULL,  -- Updated to VARCHAR(8) to match the course table
            PRIMARY KEY (sect_id, course_num),
            FOREIGN KEY (course_num) REFERENCES course(course_num),
            FOREIGN KEY (instruct_id) REFERENCES instructor(instruct_id)  -- Corrected 'REFERENCES'
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS evaluation (
            sem_year INT UNSIGNED NOT NULL,
            sem_term VARCHAR(6) NOT NULL,
            sect_id INT UNSIGNED NOT NULL,
            eval_obj VARCHAR(50),
            eval_description VARCHAR(500),
            obj_code INT UNSIGNED, 
            course_num VARCHAR(8) NOT NULL,
            instruct_id INT UNSIGNED,
            deg_name VARCHAR(50),
            deg_level VARCHAR(50),
            num_A INT UNSIGNED,
            num_B INT UNSIGNED,
            num_C INT UNSIGNED,
            num_F INT UNSIGNED,
            PRIMARY KEY (sem_year, sem_term, sect_id, obj_code, course_num, deg_name, deg_level)
        )
        """,
        """
        SET FOREIGN_KEY_CHECKS = 1;
        """
    ]

    # Execute SQL commands

    for query in create_table_queries:
        c.execute(query)


# Data entry
def enterDegree(c, info):
    print(info)
    query = 'INSERT INTO degree (deg_name, deg_level) VALUES (%s, %s)'
    c.execute(query, info)


def enterCourse(c, info):
    query = 'INSERT INTO course (course_num, course_name) VALUES (%s,%s)'
    c.execute(query, info)


def enterDegCourse(c, info):
    query = '''
    INSERT INTO degree_course (deg_name, deg_level, course_num, is_core)
    VALUES (%s, %s, %s, %s);
    '''
    c.execute(query, info)


def enterInstructor(c, info):
    query = 'INSERT INTO instructor (instruct_id, instruct_name) VALUES (%s,%s)'
    c.execute(query, info)


def enterSection(c, info):
    query = '''
    INSERT INTO section (sect_id, num_studs, sem_year, sem_term, instruct_ID, course_num) 
    VALUES (%s, %s, %s, %s, %s, %s)
    '''
    c.execute(query, info)


def enterObjective(c, info):
    query = '''
    INSERT INTO learning_obj (lo_title, description) VALUES (%s, %s)
    '''
    c.execute(query, info)


def enterObjCourse(c, info):
    query = '''
    INSERT INTO obj_course (course_num, obj_code)
    VALUES (%s, %s);
    '''
    c.execute(query, info)


def enterEvaluation(c, info):
    query = '''
    INSERT INTO evaluation (sem_year, sem_term, sect_id, eval_obj, eval_description, obj_code, course_num, instruct_id, deg_name, deg_level, num_A, num_B, num_C, num_F)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
    c.execute(query, info)


# Query
def getInstructorSections(c, info):
    query = '''
    SELECT 
        sect_id, 
        course_num, 
        sem_term, 
        sem_year
    FROM 
        section 
    WHERE 
        instruct_id = %s AND
        (
            (sem_year > %s AND sem_year < %s)  -- Years fully between start and end year
            OR (sem_year = %s AND sem_term >= %s)  -- Start year, from 'Fall' onwards
            OR (sem_year = %s AND sem_term <= %s)  -- End year, up to 'Spring'
        )

    '''
    # params = (instructor_id, start_year - 1, end_year + 1, start_year, start_term, end_year, end_term)
    
    c.execute(query, info)
    return c.fetchall()

def getCourseSections(c, info):
    query = '''
    SELECT 
        sect_id, 
        course_num, 
        sem_term, 
        sem_year
    FROM 
        section 
    WHERE 
        course_num = %s AND
        (
            (sem_year > %s AND sem_year < %s) 
            OR (sem_year = %s AND sem_term >= %s) 
            OR (sem_year = %s AND sem_term <= %s)  
        )

    '''
    # params = (instructor_id, start_year - 1, end_year + 1, start_year, start_term, end_year, end_term)
    
    c.execute(query, info)
    return c.fetchall()

def getLearningObjectivesForDegree(c, info):
    query = '''
    SELECT DISTINCT lo.obj_code, lo.lo_title, lo.description
    FROM learning_obj lo
    JOIN obj_course oc ON lo.obj_code = oc.obj_code
    JOIN degree_course dc ON oc.course_num = dc.course_num
    WHERE dc.deg_name = %s AND dc.deg_level = %s;
    '''
    c.execute(query, info)
    return c.fetchall()


def listCoursesByObjectives(c, info):
    query = '''
    SELECT obj_course.obj_code, degree_course.course_num
    FROM obj_course
    JOIN degree_course ON obj_course.course_num = degree_course.course_num
    WHERE degree_course.deg_name = %s AND degree_course.deg_level = %s;
    '''
    c.execute(query, info)
    return c.fetchall()

def getEval(c, info):
    print(info)
    query = '''
    SELECT
        e.course_num, e.sect_id, e.obj_code, e.eval_obj, e.num_A, e.num_B, e.num_C, e.num_F, e.eval_description
    FROM
        Evaluation e
    WHERE
        e.deg_name = %s AND
        e.deg_level = %s AND 
        e.sem_year = %s AND  
        e.sem_term = %s AND
        e.instruct_ID = %s;
    '''
    c.execute(query, info)
    result = c.fetchall()
    print(result)
    return result

def collectObjCodeFromCourse(c, info):
    query = '''
    SELECT obj_code
    FROM obj_course
    WHERE course_num = %s;
    '''
    c.execute(query, info)
    return c.fetchall()

def collectDegFromCourse(c, info):
    query = '''
    SELECT deg_name, deg_level
    FROM degree_course
    WHERE course_num = %s;
    '''
    c.execute(query, info)
    return c.fetchall()

def addEvalSkeleton(c, info):
    results = collectObjCodeFromCourse(c, info[3])
    degResults = collectDegFromCourse(c, info[3])
    for deg in degResults:
        temp1 = info + deg
        for obj in results:
            temp = temp1 + obj
            query = '''
            INSERT INTO evaluation (sem_year, sem_term, sect_id, course_num, instruct_id, deg_name, deg_level, obj_code)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            '''
            c.execute(query, temp)

def updateEvaluation(c, info):
    query = '''
    UPDATE Evaluation
    SET eval_description = %s, eval_obj = %s, num_A = %s, num_B = %s, num_C = %s, num_F = %s 
    WHERE sem_year = %s AND sem_term = %s AND course_num = %s and sect_id = %s AND obj_code = %s AND deg_name = %s AND deg_level = %s;
    '''
    c.execute(query, info)

def giveNumOfStuds(c, info, percentage):
    print(info)
    print(percentage)
    query = '''
    SELECT
        s.sect_id,
        s.course_num,
        s.num_studs,
        e.num_F
    FROM Section s
    JOIN Evaluation e ON s.sect_id = e.sect_id
        AND s.course_num = e.course_num
        AND s.sem_year = e.sem_year
        AND s.sem_term = e.sem_term
    WHERE s.sem_term = %s
    AND s.sem_year = %s;
    '''
    c.execute(query, info)
    results = c.fetchall()
    print(results)
    temp = []
    toReturn = []
    for result in results:
        if result[2] == None or result[3] == None:
            continue
        if result[3] > result[2] or result[2] == 0:
            passPercent = 0
        else:
            passPercent = (1-(result[3]/result[2]))
        if passPercent >= int(percentage)/100:
            temp.append(result)
    for entry in temp:
        toReturn.append((entry[0], entry[1], f"{(int)(100*passPercent)}%"))

    print(toReturn)
    return toReturn


def fromDegreeGetCourse(c, info):
    query = '''
    SELECT
        Course.course_num,
        Degree_Course.is_core
    FROM
        Degree_Course
    JOIN
        Course ON Degree_Course.course_num = Course.course_num
    WHERE
        Degree_Course.deg_name = %s AND Degree_Course.deg_level = %s;
    '''
    c.execute(query, info)
    return c.fetchall()

def fromDegreeGetSects(c, info):
    query = '''
    SELECT s.sect_id, s.course_num, s.sem_term, s.sem_year
    FROM Section s
    JOIN degree_course dc ON s.course_num = dc.course_num
    WHERE dc.deg_name = %s AND dc.deg_level = %s     
    ORDER BY s.sem_year, 
             CASE s.sem_term 
                 WHEN 'Fall' THEN 1 
                 WHEN 'Spring' THEN 2 
                 WHEN 'Summer' THEN 3 
                 ELSE 4 
             END;
    '''
    c.execute(query, info)
    return c.fetchall()

def fromDegreeGetObj(c, info):
    query = '''
    SELECT
        obj_code,
        lo_title,
        description
    FROM
        learning_obj;
    '''
    c.execute(query, info)
    return c.fetchall()

def fromCourseGetSection(c, info):
    query = '''
    SELECT s.* 
        FROM Section s
        JOIN Degree_Course dc ON s.course_num = dc.course_num
        WHERE dc.deg_name = %s AND dc.deg_level = %s     
        ORDER BY s.sem_year, 
                 CASE s.sem_term 
                     WHEN 'Fall' THEN 1 
                     WHEN 'Spring' THEN 2 
                     WHEN 'Summer' THEN 3 
                     ELSE 4 
                 END;
    '''
    c.execute(query, info)
    return c.fetchall()

def fromInstructorGetSections(c, info):
    query = '''
    SELECT 
        s.sect_id, s.course_num
    FROM 
        Section s
    JOIN 
        Instructor i ON s.instruct_id = i.instruct_id
    WHERE 
        i.instruct_id = %s AND s.sem_year = %s  AND s.sem_term = %s;
    '''
    c.execute(query, info)
    return c.fetchall()

# Get all data for debug
def getAllDegree(c):
    query = '''select * from degree'''
    c.execute(query)
    return c.fetchall()


def clearDegree(c):
    query = '''delete from degree'''
    c.execute(query)
    return c.fetchall()


# Get all entries in a table
def getTable(c, name):
    query = f'''select * from {name}'''
    c.execute(query)
    return c.fetchall()


# Clear all entries in a table
def clearTable(c, name):
    query = f'''delete from {name}'''
    c.execute(query)


def clearAll(c):
    c.execute("SHOW TABLES")
    tables = c.fetchall()

    for table in tables:
        table_name = table[0]
        c.execute(f"DELETE FROM {table_name}")
        print(f"All entries cleared from table: {table_name}")


def dropAll(c):
    c.execute(f"USE {db_name}")
    c.execute("SHOW TABLES")
    tables = c.fetchall()

    for table in tables:
        table_name = table[0]
        c.execute("SET FOREIGN_KEY_CHECKS = 0")
        c.execute(f"DROP TABLE {table_name}")
        print(f"{table_name} dropped")

# def listCoursesByObjectives(c, info):
#     query = """
#     SELECT lo.lo_title AS Objective, GROUP_CONCAT(dc.course_num ORDER BY dc.course_num) AS Courses
#     FROM learning_obj lo
#     JOIN obj_course oc ON lo.obj_code = oc.obj_code
#     JOIN degree_course dc ON oc.course_num = dc.course_num
#     WHERE dc.deg_name = %s
#     GROUP BY lo.lo_title;
#     """
#     c.execute(query, info)
#     return c.fetchall()


# def driver(cr, filename):
#     with open(filename, newline='') as csvfile:
#         cmdReader = csv.reader(csvfile, delimiter=',', quotechar='|', skipinitialspace=True)
#         cmd = ""
#         for row in cmdReader:
#             cmd = row[0]
#             match cmd:
#                 # data manipulation cases
#                 case 'e':
#                     e(cr)
#                     continue
#                 case 'r':
#                     r(cr)
#                     continue
#                 case 'p':
#                     p(cr, row)
#                     continue
#                 case 'm':
#                     m(cr, row)
#                     continue
#                 case 'n':
#                     n(cr, row)
#                     continue
#                 case 'c':
#                     c(cr, row)
#                     continue
#
#                 # queries
#                 case 'P':
#                     P(cr, row)
#                 case 'A':
#                     A(cr, row)
#                 case 'D':
#                     D(cr, row)
#                 case 'M':
#                     M(cr, row)
#                 case _:
#                     print("Invalid command given. Skipping line.")
#     # print(','.join(row))


# dir_path = os.path.dirname(os.path.realpath(__file__))
# fileName = input(f'Where is your file located relative to {dir_path}?\n')
# default = 'test1.csv'
# load_dotenv()
# PASSWORD = getenv('PASSWORD')
# USER = getenv('USER')
def connect_to_db():
    try:
        cn = pymysql.connect(
            host='localhost',
            user='root',
            password=db_password,
            client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS,
            autocommit=True
        )
        print("Connection successful!")
    except pymysql.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

    create_schema_sql = f"CREATE SCHEMA IF NOT EXISTS {db_name}"
    create_database_sql = f"CREATE DATABASE IF NOT EXISTS {db_name}"

    cr = cn.cursor()
    dropAll(cr)
    cr.execute(create_schema_sql)
    cr.execute(create_database_sql)
    createTables(cr)
    print(db_name)
    # nicoPlayground.populateTestData(cr)
    cr.execute(f"USE {db_name}")


    return cr, cn


def close_db(cn: pymysql.connections.Connection):
    # cn.commit()
    cn.close()

# cr.execute('CREATE DATABASE IF NOT EXISTS dbprog')


# driver(cr, default)

# cn.close()



# cr = controller.cursor

#         tk.Frame.__init__(self, parent)
#         self.name = name
#         label = tk.Label(self, text=name)
#         label.grid(row=0, column=0, columnspan=4)

#         ttk.Label(self, text="Name", anchor="center").grid(row=1, column=0)
#         self.entry_name = ttk.Entry(self)
#         self.entry_name.grid(row=1, column=1)
#         ttk.Label(self, text="Level", anchor="center").grid(row=1, column=2)
#         self.entry_level = ttk.Entry(self)
#         self.entry_level.grid(row=1, column=3)

        

#         tk.Button(self, text="Search",
#                   command=lambda: (
#                         info := (self.entry_name.get(), self.entry_level.get()),
#                         populateTree(self.treeCourse, q.fromDegreeGetCourse(cr, info)),
#                         populateTree(self.treeSect, q.fromDegreeGetSects(cr, info)),
#                         populateTree(self.treeObj, q.getLearningObjectivesForDegree(cr, info)),
#                         populateTree(self.treeCO, q.listCoursesByObjectives(cr, info))
#                   )
#                   ).grid(row=1, column=5)

#         # info display
#         ttk.Label(self, text="Associated Courses",
#                   anchor="center").grid(row=2, column=0)
#         self.treeCourse = ttk.Treeview(
#             self, columns=("Name", "IsCore"), show="headings")
#         self.treeCourse.heading("Name", text="Course Number")
#         self.treeCourse.heading("IsCore", text="IsCore")
#         self.treeCourse.grid(row=3, column=0, columnspan=2)