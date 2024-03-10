import sqlite3 
# self-explanatory, yes?
connector = sqlite3.connect('schStudent.db')

c = connector.cursor()

# c.execute("""CREATE TABLE studentDB(
#     studentID int NOT NULL,
#     firstName text,
#         lastName text,
#         dob text,
#         classRoom text, 
#         homeRoom text,
#         teacherName text,
#         guardianName text,
#         PRIMARY KEY (studentID)
# )""")

query = c.execute("""SELECT * FROM studentDB""")
for row in query.fetchall():
    print(row)
    
connector.close()