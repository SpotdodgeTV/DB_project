import pymysql
import pymysql.cursors
import os
from dotenv import load_dotenv
import nicoPlayground

load_dotenv()
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')


# data manipulation commands
def createTables(c):
    create_table_queries = [
        """
        CREATE TABLE IF NOT EXISTS section (
            sect_id INT AUTO_INCREMENT PRIMARY KEY,
            num_studs INT,
            sem_year INT NOT NULL,
            sem_term VARCHAR(6) NOT NULL,
            instruct_id INT NOT NULL,
            course_num VARCHAR(6) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS learning_obj (
            obj_code INT AUTO_INCREMENT PRIMARY KEY,
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
            PRIMARY KEY (course_num, deg_name, deg_level)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS obj_course (
            obj_code INT NOT NULL,
            course_num VARCHAR(8) NOT NULL,
            PRIMARY KEY (obj_code, course_num)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS semester (
            year INT NOT NULL,
            term VARCHAR(6) NOT NULL,
            PRIMARY KEY (year, term)  -- Added primary key constraint
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS instructor (
            instruct_id INT NOT NULL PRIMARY KEY,
            instruct_name VARCHAR(50) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS evaluation (
            sem_year INT NOT NULL,
            sem_term VARCHAR(6) NOT NULL,
            sect_id INT NOT NULL,
            eval_obj VARCHAR(50) NOT NULL,
            eval_description VARCHAR(500),
            obj_code INT, 
            course_num VARCHAR(6) NOT NULL,
            instruct_id INT,
            num_A INT,
            num_B INT,
            num_C INT,
            num_F INT,
            PRIMARY KEY (sem_year, sem_term, sect_id, eval_obj, course_num)
        )
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
    INSERT INTO evaluation (sem_year, sem_term, sect_id, eval_obj, eval_description, obj_code, course_num, instruct_id, num_A, num_B, num_C, num_F)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
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
    query = '''
    SELECT
        e.section_ID,
        e.course_number,
        e.eval_obj,
        e.#_A as NumberOfA,
        e.#_B as NumberOfB,
        e.#_C as NumberOfC,
        e.#_F as NumberOfF,
        e.eval_descript,
        e.deg_name,
        e.deg_lvl 
    FROM
        Evaluation e
    JOIN
        Section s ON e.section_ID = s.Section_ID AND e.instruct_ID = s.instruct_ID
    WHERE
        e.instruct_ID = ? AND 
        s.sem_year = ? AND  
        s.sem_term = ?; 
    '''
    c.execute(query)


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
    nicoPlayground.populateTestData(cr)
    cr.execute(f"USE {db_name}")


    return cr, cn


def close_db(cn: pymysql.connections.Connection):
    # cn.commit()
    cn.close()

# cr.execute('CREATE DATABASE IF NOT EXISTS dbprog')


# driver(cr, default)

# cn.close()
