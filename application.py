import psycopg2
import string

# Connect to your postgres DB
conn = psycopg2.connect("dbname=students user=postgres password=student host=localhost port=5432")

# Open a cursor to perform database operations
cur = conn.cursor()

#Retrieves and displays all records from the students table.
def getAllMember(): 
    # Execute a query
    cur.execute("SELECT * FROM members")
    # Retrieve query results
    members = cur.fetchall()
    #print each row of students
    for member in members:
        print(member)
getAllMembers()

def getMemberInfo():
        
        memberUser  = input("Enter member username: ")
        memberPass = input("Enter member password: ")
        cur.execute("SELECT * FROM members WHERE username = (%s) AND password = (%s) ;", 
                    (memberUser, memberPass))

        member = cur.fetchone()

        if member:
            print("Member found:", member)
        else:
            print("Member not found.")
            
getMemberbyInfo()
