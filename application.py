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

def getMemberbyID():     
        memberUser  = input("\nEnter member username: ")
        memberPass = input("Enter member password: ")
        cur.execute("SELECT * FROM members WHERE username = (%s) AND password = (%s) ;", 
                    (memberUser, memberPass))

        member = cur.fetchone()
        member_id = member[0]
        
        if member:
            print("Member found:", member)
            return member_id
        else:
            print("Member not found.")
            
def login():
    memberUser = input("Enter member username: ")
    memberPass = input("Enter member password: ")
    cur.execute("SELECT * FROM members WHERE username = (%s) AND password = (%s) ;", 
        (memberUser, memberPass))
    member = cur.fetchone()
    return member

def getMemberInfo():
        member = login()
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

#getting this to work with the other function with proper sequence
def update_member_info():
    user_input = input("Would you like to update your information? (Y | N): ")

    while True:
        if user_input == "Y":
            print("Please enter the following information to update your profile:")
            fitness_goal = int(input("New Fitness Goal: "))
            weight = int(input("New Weight (lbs): "))
            height = int(input("New Height (cm): "))
            achieved_date = input("New date to achieve by: ")
            cur.execute("UPDATE members SET goal_weight = %s, curr_weight = %s, height = %s, achieved_date = %s",
                    (fitness_goal, weight, height, achieved_date))
            break
        else:
            break

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
        members_count = 0
        type_class_pick = int(input("\nPick 1 for personal classes and 2 for group classes ")) 
        
        if type_class_pick == 1:
             getAllPersonalClasses()
             personal_class_id = input("\nEnter Personal Class ID you'd like to register in: ")     

             cur.execute("SELECT * FROM personal_classes WHERE personal_classes_id = (%s) ;", 
                    (personal_class_id))

             personal_class = cur.fetchone()
            
             if personal_class:
                print("\nPersonal Class ID found:", personal_class_id)
                member_by_id=getMemberbyID()
                #if class exists, choose a trainer
                getAllTrainers()
                trainer_id = input("\nPick a trainer for your personal class: ")
                cur.execute("SELECT trainer_id FROM trainers WHERE trainer_id = %s",  (trainer_id,))
                #set the trainer's availiblity to this personal class session
                cur.execute("SELECT available FROM trainers WHERE trainer_id = %s", (trainer_id,))
                available=cur.fetchone()
                cur.execute("UPDATE personal_classes SET available = (%s) WHERE personal_classes_id = (%s);", 
                               (available, personal_class_id))
                
                # Set member ID and trainer ID for the personal class
                cur.execute("UPDATE personal_classes SET member_id = %s, trainer_id = %s WHERE personal_classes_id = %s;",
                            (member_by_id, trainer_id, personal_class_id))
                
                cur.execute("SELECT * FROM personal_classes WHERE personal_classes_id = (%s) ;", 
                               (personal_class_id))
                print("You've successfully registered for the class")
                
                print("Member ID: ",member_by_id,"registered with trainer ID:", trainer_id)
                getAllPersonalClasses()
               
             else:
                print("Personal class ID not found.")

        elif type_class_pick == 2 :
            getAllGroupClasses()
            group_class_id = input("\nEnter Group Class ID you'd like to register in: ")
        
            cur.execute("SELECT * FROM group_classes WHERE group_classes_id = (%s) ;", 
                            (group_class_id))

            group_class = cur.fetchone()
            
            if group_class:
                print("\nGroup Class ID found:", group_class_id)
                #increase member count in group class
                members_count += 1
                
                cur.execute("UPDATE group_classes SET members_count = (%s) WHERE group_classes_id = (%s);", 
                                  (members_count, group_class_id))
                cur.execute("SELECT max_members FROM group_classes WHERE group_classes_id = (%s);",
                                   (group_class_id,))
                #find max members value for current group class id and check if capacity has reached before registering
                max_members=cur.fetchone()[0]
                print("max members:", max_members)
                print("member count:", members_count)
                if members_count<max_members :
                    print("You've successfully registered for the class")
                else:
                    print("Sorry class is full :(")
            else:
                print("Group class ID not found.")
        else:
            print("Enter a correct option")

