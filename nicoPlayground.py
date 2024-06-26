import pymysql
import query as q


def populateTestData(c):
    # Insert data into 'degree'
    degrees = [
        ('Computer Science', 'BS'),
        ('Mathematics', 'BS'),
        ('Engineering', 'BS')
    ]
    for degree in degrees:
        c.execute("INSERT INTO degree (deg_name, deg_level) VALUES (%s, %s);", degree)

    # Insert data into 'course'
    courses = [
        ('CS101', 'Intro to Computer Science'),
        ('CS102', 'Data Structures'),
        ('MA101', 'Calculus I'),
        ('EN101', 'Intro to Engineering')
    ]
    for course in courses:
        c.execute("INSERT INTO course (course_num, course_name) VALUES (%s, %s);", course)

    # Insert data into 'degree_course'
    degree_courses = [
        ('Computer Science', 'BS', 'CS101', True),
        ('Computer Science', 'BS', 'CS102', True),
        ('Mathematics', 'BS', 'MA101', True),
        ('Engineering', 'BS', 'EN101', True),
        ('Mathematics', 'BS', 'CS101', False)
    ]
    for dc in degree_courses:
        c.execute("INSERT INTO degree_course (deg_name, deg_level, course_num, is_core) VALUES (%s, %s, %s, %s);", dc)

    # Insert data into 'learning_obj'
    learning_objs = [
        ('Programming Fundamentals', 'Learn basic programming concepts'),
        ('Data Structures Concepts', 'Understand various data structures'),
        ('Calculus Concepts', 'Understand the basics of calculus'),
        ('Engineering Principles', 'Learn fundamental engineering concepts')
    ]
    for lo in learning_objs:
        c.execute("INSERT INTO learning_obj (lo_title, description) VALUES (%s, %s);", lo)

    # Insert data into 'obj_course'
    obj_courses = [
        (1, 'CS101'),
        (1, 'MA101'),
        (4, 'CS101'),
        (2, 'CS102'),
        (1, 'CS102'),
        (3, 'MA101'),
        (4, 'EN101')
    ]
    for oc in obj_courses:
        c.execute("INSERT INTO obj_course (obj_code, course_num) VALUES (%s, %s);", oc)

    instructors = [
        (1234, "Klyne Smith"),
        (4321, "King Ip Lin")
    ]
    for inst in instructors:
        c.execute("INSERT INTO instructor (instruct_id, instruct_name) VALUE (%s, %s)", inst)

    sections = [
        (1, 20, 2024, "Fall", 1234, "CS101"),
        (6, 20, 2024, "Spring", 1234, "CS101"),
        (2, 20, 2023, "Fall", 1234, "CS101")
    ]
    for sect in sections:
        c.execute("INSERT INTO section (sect_id, num_studs, sem_year, sem_term, instruct_ID, course_num) VALUES (%s, %s, %s, %s, %s, %s)", sect)


    evaluations = [
        # (2024, "Fall", 1, "Homework", "You suck", 1, "CS101", 1234, "Computer Science", "BS", 5, 5, 5, 5),
        (2023, "Fall", 2, "Homework", "You suck LMAO", 1, "CS101", 1234, "Computer Science", "BS", 5, 5, 5, 5)
    ]
    
    for eval in evaluations:
        q.enterEvaluation(c, eval)
    # Commit changes to the database
    # c.connection.commit()

def listCoursesByObjectives(c, degree_name, deg_level):
    query = """
    SELECT lo.lo_title AS Objective, GROUP_CONCAT(dc.course_num ORDER BY dc.course_num) AS Courses
    FROM learning_obj lo
    JOIN obj_course oc ON lo.obj_code = oc.obj_code
    JOIN degree_course dc ON oc.course_num = dc.course_num
    WHERE dc.deg_name = %s AND dc.deg_level = %s
    GROUP BY lo.lo_title;
    """
    c.execute(query, (degree_name, deg_level))
    return c.fetchall()


def getLearningObjectivesForDegree(c, deg_name, deg_level):
    query = """
    SELECT DISTINCT lo.obj_code, lo.lo_title, lo.description
    FROM learning_obj lo
    JOIN obj_course oc ON lo.obj_code = oc.obj_code
    JOIN degree_course dc ON oc.course_num = dc.course_num
    WHERE dc.deg_name = %s AND dc.deg_level = %s;
    """
    c.execute(query, (deg_name, deg_level))
    return c.fetchall()


cr, cn = q.connect_to_db()
q.dropAll(cr)
q.createTables(cr)
if cr is None:
    print("Table creation failed.")

# degreeData = [
#     ("cs", "PHD"),
#     ("eng", "MS"),
#     ("art", "BA"),
#     ("math", "BS")
# ]

# for degree in degreeData:
#     q.enterDegree(cr, degree)

# result = q.getAllDegree(cr)
# print(result)
# print(len(result))

# courseData = [
#     ("CS1234", "Intro to Computer Science"),
#     ("EN4321", "Creative Writing"),
#     ("AR2233", "How to Use a Pencil"),
#     ("MA1324", "Math 101: Calculating Quantum Topology")
# ]

# for course in courseData:
#     q.enterCourse(cr, course)

# result = q.getTable(cr, "course")
# print(result)
# print(len(result))

populateTestData(cr)

# print(listCoursesByObjectives(cr, "Computer Science", "BS"))
# print(getLearningObjectivesForDegree(cr, "Computer Science", "BS" ))
# print(q.fromDegreeGetCourse(cr, ("Mathematics", "BS")))
# print(q.getInstructorSections(cr, 1234, 2000, "Fall", 2050, "Spring"))
# print(q.listCoursesByObjectives(cr, ("Computer Science", "BS")))

# print(q.getEval(cr, ("Computer Science", "BS", 2024, "Fall", 1234)))


q.addEvalSkeleton(cr, (2024, "Fall", 1, "CS101", 1234))
q.updateEvaluation(cr, ("kys", "test", 5, 5, 5, 5, 2024, "Fall", "CS101", 1, 1, "Computer Science", "BS"))
q.updateEvaluation(cr, ("kys", "test", 5, 5, 5, 5, 2024, "Fall", "CS101", 1, 1, "Mathematics", "BS"))


print(q.getEval(cr, ("Computer Science", "BS", 2024, "Fall", 1234, )))
print(q.getEval(cr, ("Mathematics", "BS", 2024, "Fall", 1234, )))

print(q.giveNumOfStuds(cr, ("Fall", 2024), .7))

q.close_db(cn)
