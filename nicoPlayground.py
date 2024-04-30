import pymysql
# import query as q


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
        ('Engineering', 'BS', 'EN101', True)
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


# cr, cn = q.connect_to_db()
# q.dropAll(cr)
# q.createTables(cr)
# if cr is None:
#     print("Table creation failed.")

# # degreeData = [
# #     ("cs", "PHD"),
# #     ("eng", "MS"),
# #     ("art", "BA"),
# #     ("math", "BS")
# # ]

# # for degree in degreeData:
# #     q.enterDegree(cr, degree)

# # result = q.getAllDegree(cr)
# # print(result)
# # print(len(result))

# # courseData = [
# #     ("CS1234", "Intro to Computer Science"),
# #     ("EN4321", "Creative Writing"),
# #     ("AR2233", "How to Use a Pencil"),
# #     ("MA1324", "Math 101: Calculating Quantum Topology")
# # ]

# # for course in courseData:
# #     q.enterCourse(cr, course)

# # result = q.getTable(cr, "course")
# # print(result)
# # print(len(result))

# populateTestData(cr)

# print(listCoursesByObjectives(cr, "Computer Science", "BS"))
# print(getLearningObjectivesForDegree(cr, "Computer Science", "BS" ))
# q.close_db(cn)
