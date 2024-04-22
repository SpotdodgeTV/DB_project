import pymysql
import pymysql.cursors
from pymysql import connect
#from dotenv import load_dotenv
import os
from os import getenv
import csv
from datetime import datetime

def convertTime(date, hasTime=True):
    try:
        if hasTime:
            parsedDate = datetime.strptime(date, "%Y%m%d:%H:%M:%S")
            mysqlDatetime = parsedDate.strftime("%Y-%m-%d %H:%M:%S")
            return mysqlDatetime
        else:
            parsedDate = datetime.strptime(date, "%Y%m%d")
            mysqlDatetime = parsedDate.strftime("%Y-%m-%d")
            return mysqlDatetime
    except ValueError:
        print("Error: Invalid date format. Please provide the date in the format 'yyyymmdd:hh:mm:ss' or 'yymmdd'")
        return date


# data manipulation commands
def init(c):
    create_schema_sql = f"CREATE SCHEMA IF NOT EXISTS {dbname}"
    create_database_sql = f"CREATE DATABASE IF NOT EXISTS {dbname}"
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS section (
        section_id INT AUTO_INCREMENT PRIMARY KEY,
        num_of_students INT,
        sem_year INT NOT NULL,
        sem_term VARCHAR(6) NOT NULL,
        instruct_id INT NOT NULL,
        course_num VARCHAR(6) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS objective (
        obj_code INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(50) NOT NULL UNIQUE,
        description VARCHAR(300)
    );
    
    CREATE TABLE IF NOT EXISTS degree (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        level VARCHAR(10) NOT NULL,
    );
    
    CREATE TABLE IF NOT EXISTS course (
        code VARCHAR(8) NOT NULL PRIMARY KEY,
        name VARCHAR(50) NOT NULL UNIQUE,
    );
    
    CREATE TABLE IF NOT EXISTS degree_course (
        course_code VARCHAR(8) NOT NULL,
        degree_id INT NOT NULL,
        is_core BOOL,
        FOREIGN KEY (course_code) REFERENCES course(code),
        FOREIGN KEY (degree_id) REFERENCES degree(id),
        (course_code, degree_id) PRIMARY KEY
    );
    
    CREATE TABLE IF NOT EXISTS obj_course (
        name VARCHAR(50) NOT NULL,
        level VARCHAR(10) NOT NULL,
        PRIMARY KEY (name, level)
    );
    
    CREATE TABLE IF NOT EXISTS semester (
        year INT NOT NULL,
        term VARCHAR(6) NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS instructor (
        id INT NOT NULL,
        name VARCHAR(50) NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS evaluation (
        sem_year INT NOT NULL,
        sem_term VARCHAR(6) NOT NULL,
        section_id INT,
        eval_obj VARCHAR(50) NOT NULL,
        obj_code INT, 
        course_num VARCHAR(6) NOT NULL,
        instruct_id INT NOT NULL,
        num_A INT NOT NULL,
        num_B INT NOT NULL,
        num_C INT NOT NULL,
        num_F INT NOT NULL
    );
    """

    # Execute SQL commands
    c.execute(create_schema_sql)
    c.execute(create_database_sql)
    c.execute(f"USE {dbname}")  # Switch to your database
    c.execute(create_table_sql)


def e(c):
    createPlayerTable = '''
    CREATE TABLE IF NOT EXISTS Player (
        ID INT PRIMARY KEY,
        Name VARCHAR(255) UNIQUE,
        Birthdate DATE,
        Rating INT,
        State CHAR(2)
    );
    '''
    createMatchesTable = '''
    CREATE TABLE IF NOT EXISTS Matches (
        HostID INT,
        GuestID INT,
        Start DATETIME,
        End DATETIME,
        Hostwin BOOLEAN,
        PreRatingHost INT,
        PostRatingHost INT,
        PreRatingGuest INT,
        PostRatingGuest INT
    );'''
    c.execute(createPlayerTable)
    c.execute(createMatchesTable)


def r(c):
    deletePlayerEntries = '''
    DELETE FROM Player;
    '''
    deleteMatchesEntries = '''
    DELETE FROM Matches;
    '''
    c.execute(deletePlayerEntries)
    c.execute(deleteMatchesEntries)

def p(c, row):
    cmd = f'''
    INSERT INTO player (ID, Name, Birthdate, Rating, State)
        VALUES ({row[1]}, '{row[2]}', {row[3]}, {row[4]}, '{row[5]}');
    '''
    c.execute(cmd)


def m(c, row):
    row[3] = convertTime(row[3])
    row[4] = convertTime(row[4])
    cmd = f'''
    INSERT INTO Matches (HostID, GuestID, Start, End, Hostwin, PreRatingHost, PostRatingHost, PreRatingGuest, PostRatingGuest)
        VALUES ({row[1]}, {row[2]}, '{row[3]}', '{row[4]}', {row[5]}, {row[6]}, {row[7]}, {row[8]}, {row[9]});
    '''
    c.execute(cmd)

def n(c, row):
    row[3] = convertTime(row[3])
    cmd = f'''
    INSERT INTO Matches (HostID, GuestID, Start, End, Hostwin, PreRatingHost, PostRatingHost, PreRatingGuest, PostRatingGuest)
        VALUES ({row[1]}, {row[2]}, '{row[3]}', NULL, NULL, NULL, NULL, NULL, NULL);
    '''
    c.execute(cmd)

def c(c, row):
    row[3] = convertTime(row[3])
    row[4] = convertTime(row[4])
    cmd = f'''
    UPDATE Matches
    SET End = '{row[4]}', Hostwin = {row[5]}, PreRatingHost = {row[6]}, PostRatingHost = {row[7]}, PreRatingGuest = {row[8]}, PostRatingGuest = {row[9]}
    WHERE HostID = {row[1]}
    AND GuestID = {row[2]}
    AND Start = '{row[3]}';
    '''
    c.execute(cmd)


# query helper function
def stringify(row):
    result = []
    for item in row:
        if not isinstance(item, str):
            result.append(str(item))
        else:
            result.append(item)
    return tuple(result)


def execAndPrint(c, cmd, fetchOne=True, indent=True):
    c.execute(cmd)
    if fetchOne:
        row = c.fetchone()
        row = stringify(row)
        print(", ".join(row))
    else:
        rows = c.fetchall()
        for row in rows:
            row = stringify(row)
            if indent:
                print("\t" + ", ".join(row))
            else:
                print(", ".join(row))


# queries
def P(c, row):
    cmd=f'''
    SELECT Name, DATE_FORMAT(Birthdate, '%Y-%m-%d') AS FormattedBirthdate, Rating, State
    FROM player
    WHERE ID = {row[1]};
    '''
    execAndPrint(c, cmd)
    print('')


def A(c, row):
    getName = f'''
    SELECT ID, Name
    FROM player
    WHERE ID = {row[1]};
    '''

    getWL = f'''
    SELECT 
    op.ID AS ID,
    op.Name AS Name,
    SUM(CASE 
            WHEN m.HostID = p.ID AND m.Hostwin = 1 THEN 1
            WHEN m.GuestID = p.ID AND m.Hostwin = 0 THEN 1
            ELSE 0 
        END) AS Wins,
    SUM(CASE 
            WHEN m.HostID = p.ID AND m.Hostwin = 0 THEN 1
            WHEN m.GuestID = p.ID AND m.Hostwin = 1 THEN 1
            ELSE 0 
        END) AS Losses
    FROM 
        Player p
    JOIN 
        Matches m ON p.ID = m.HostID OR p.ID = m.GuestID
    JOIN 
        Player op ON (p.ID = m.HostID AND op.ID = m.GuestID) OR (p.ID = m.GuestID AND op.ID = m.HostID)
    WHERE 
        p.ID = {row[1]}
    GROUP BY 
        op.ID, op.Name
    ORDER BY 
        op.ID;'''

    execAndPrint(c, getName)
    execAndPrint(c, getWL, False, True)
    print('')


def D(c, row):
    cmd = f'''
    SELECT
        DATE_FORMAT(m.Start, '%Y%m%d') AS Start_Date,
        DATE_FORMAT(m.End, '%Y%m%d') AS End_Date,
        TIME(m.Start) AS Start_Time,
        TIME(m.End) AS End_Time,
        h.Name AS Host_Name,
        g.Name AS Guest_Name,
        CASE WHEN m.Hostwin THEN 'H' ELSE 'G' END AS Winner
    FROM
        Matches m
    JOIN
        Player h ON m.HostID = h.ID
    JOIN
        Player g ON m.GuestID = g.ID
    WHERE
        m.Start >= {convertTime(row[1], False)} <= {convertTime(row[2], False)}
    ORDER BY
        m.Start ASC,
        m.HostID ASC;
    '''

    execAndPrint(c, cmd, False, False)
    print('')


def M(c, row):
    getName = f'''
    SELECT ID, Name
    FROM player
    WHERE ID = {row[1]};
    '''

    getMatches = f'''   
    SELECT DISTINCT 
        DATE_FORMAT(m.Start, '%Y%m%d %H:%i:%s') AS StartDateTime,
        DATE_FORMAT(m.End, '%Y%m%d %H:%i:%s') AS EndDateTime,
        CASE
            WHEN m.HostID = {row[1]} THEN m.GuestID
            ELSE m.HostID
        END AS OpponentID,
        CASE
            WHEN m.HostID = {row[1]} THEN g.Name
            ELSE h.Name
        END AS OpponentName,
        CASE
            WHEN (m.HostID = {row[1]} AND m.Hostwin = TRUE) OR (m.GuestID = {row[1]} AND m.Hostwin = FALSE) THEN 'W'
            WHEN (m.HostID = {row[1]} AND m.Hostwin = FALSE) OR (m.GuestID = {row[1]} AND m.Hostwin = TRUE) THEN 'L'
        END AS Result,
        CASE
            WHEN m.HostID = {row[1]} THEN m.PreRatingHost
            ELSE m.PreRatingGuest
        END AS PreviousMatchRating,
        CASE
            WHEN m.HostID = {row[1]} THEN m.PostRatingHost
            ELSE m.PostRatingGuest
        END AS PostMatchRating
    FROM 
        Matches m
    JOIN 
        Player p ON m.HostID = {row[1]} OR m.GuestID = {row[1]}
    JOIN 
        Player h ON m.HostID = h.ID
    JOIN 
        Player g ON m.GuestID = g.ID
    WHERE 
        (m.HostID = {row[1]} OR m.GuestID = {row[1]})
    ORDER BY 
        StartDateTime ASC;
    '''

    execAndPrint(c, getName)

    c.execute(getMatches)
    rows = c.fetchall()
    prevRating = -1
    for row in rows:
        validStr = ""
        if prevRating != -1:
            if row[5] != prevRating:
                validStr = ", inconsistent rating"
        prevRating = row[6]
        row = stringify(row)
        print("\t" + ", ".join(row) + validStr)
    print('')


def driver(cr, filename):
    with open(filename, newline='') as csvfile:
        cmdReader = csv.reader(csvfile, delimiter=',', quotechar='|', skipinitialspace=True)
        cmd = ""
        for row in cmdReader:
            cmd = row[0]
            match cmd:
                # data manipulation cases
                case 'e':
                    e(cr)
                    continue
                case 'r':
                    r(cr)
                    continue
                case 'p':
                    p(cr, row)
                    continue
                case 'm':
                    m(cr, row)
                    continue
                case 'n':
                    n(cr, row)
                    continue
                case 'c':
                    c(cr, row)
                    continue

                # queries
                case 'P':
                    P(cr, row)
                case 'A':
                    A(cr, row)
                case 'D':
                    D(cr, row)
                case 'M':
                    M(cr, row)
                case _:
                    print("Invalid command given. Skipping line.")
    #print(','.join(row))


# dir_path = os.path.dirname(os.path.realpath(__file__))
# fileName = input(f'Where is your file located relative to {dir_path}?\n')
# default = 'test1.csv'
# load_dotenv()
# PASSWORD = getenv('PASSWORD')
# USER = getenv('USER')
dbname = "dbproj"

try:
    cn = pymysql.connect(
        host='localhost',
        user='root',
        password='Thepasswordispassword1!',
        client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS,
        autocommit=True
    )
    print("Connection successful!")
except pymysql.Error as e:
    print(f"Error connecting to MySQL: {e}")

cr = cn.cursor()

init(cr)

#cr.execute('CREATE DATABASE IF NOT EXISTS dbprog')


# driver(cr, default)

cn.close()