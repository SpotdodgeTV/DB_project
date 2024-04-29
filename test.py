import pymysql
import query as q

cr, cn = q.connect_to_db()
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
