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
            print("\nMember ID:", member[0])
            print("\nHEALTH METRICS")
            print("--------------------------------------------------------------------------------------------")
            print("Name: ", member[1], " ", member[2])
            print("Height: ", member[6], " cm")
            print("Weight: ", member[4], " lbs")
            print("Goal: ", member[5], " lbs")
            print("Want to achieve this goal by: ", member[3])
        else:
            print("Member not found.")
            
getMemberInfo()

def username_exists(username):
    cur.execute("SELECT COUNT(*) FROM members WHERE username = %s", (username,))
    count = cur.fetchone()[0]
    return count > 0

def register_member():
    print("To register please enter the following information: ")
    while True:
        username = input("Username: ")
        if username_exists(username):
            print("Username already exists. Please choose a different one.")
        else:
            break

    password = input("Password: ")
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    weight = int(input("Weight (lbs): "))
    height = int(input("Height (cm): "))
    fitness_goal = int(input("Fitness Goal: "))
    achievement_date = input("Please insert the date you would like to achieve your fitness goal by (year-month-day): ")

    cur.execute("SELECT MAX(member_id) FROM members")
    max_id = cur.fetchone()[0]
    if max_id is None:
        member_id = 1
    else:
        member_id = max_id + 1

    cur.execute("INSERT INTO members (member_id, first_name, last_name, achieved_date, curr_weight, goal_weight, height, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (member_id, first_name, last_name, achievement_date, weight, fitness_goal, height, username, password))
    
    print("You have been registered successfully!")

def getAllPersonalClasses(): 
    cur.execute("SELECT * FROM personal_classes")
    personal_classes = cur.fetchall()
    print("\nPersonal Classes\n")
    for personal_class in personal_classes:
        print(personal_class)
        
def getAllGroupClasses(): 
    cur.execute("SELECT * FROM group_classes")
    group_classes = cur.fetchall()
    print("\nGroup Classes\n")
    for group_class in group_classes:
        print(group_class)

#this function is for members to pick a group or personal class, then register in one that interests them. Classes are displayed
def registerClass():      
        type_class_pick = int(input("\nPick 1 for personal classes and 2 for group classes ")) 
        
        if type_class_pick == 1:
             getAllPersonalClasses()
             userInput = input("\nEnter Personal Class ID you'd like to register in: ")
        
             cur.execute("SELECT * FROM personal_classes WHERE group_classes_id = (%s) ;", 
                    (userInput))

             personal_class = cur.fetchone()
            
             if personal_class:
                print("\Personal Class ID found:", personal_class)
             else:
                print("Personal class ID not found.")

        elif type_class_pick == 2 :
            getAllGroupClasses()
            userInput2 = input("\nEnter Group Class ID you'd like to register in: ")

            cur.execute("SELECT * FROM group_classes WHERE group_classes_id = (%s) ;", 
                            (userInput2))

            group_class = cur.fetchone()
            
            if group_class:
                print("\nGroup Class ID found:", group_class)
                print("You've successfully registered for the class")
            else:
                print("Group class ID not found.")
        else:
            print("ERROR: Enter a correct option")
registerClass()
