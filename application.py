import psycopg2
import string

# Connect to your postgres DB
conn = psycopg2.connect("dbname=FinalProject user=postgres password=student host=localhost port=5432")

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
getAllMember()

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
        
def getAllTrainers(): 
    cur.execute("SELECT * FROM trainers")
    trainers = cur.fetchall()
    print("\nTrainers\n")
    for trainer in trainers:
        print(trainer)

def getTrainerByID(trainer_id): 
    cur.execute("SELECT * FROM trainers WHERE trainer_id = %s", (trainer_id,))
    trainer = cur.fetchall()
    return trainer
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
             #check if trainer is available
             if personal_class:
                print("\nPersonal Class ID found:", personal_class_id)
                member_by_id=getMemberbyID()
                generate_invoice(member_by_id, )
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
            
#Trainer pics which class they want to train  
def scheduleTrainer():
  getAllTrainers()
  user_input=int(input("Which Trainer ID are you: "))
  trainer=getTrainerByID(user_input) 
  
  user_input2=int(input("Would you like to train a personal (1) or group class (2)"))
  if user_input2==1:
    getAllPersonalClasses()
    user_input3=int(input("Pick a class to teach"))
    
    #set the trainer's availiblity to this personal class session
    cur.execute("SELECT available FROM trainers WHERE trainer_id = %s", (user_input,))
    available=cur.fetchone()
    cur.execute("UPDATE personal_classes SET available = (%s) WHERE personal_classes_id = (%s);", 
              (available, user_input3))
  
  elif user_input2==2:
     getAllGroupClasses()
     user_input4=int(input("Pick a class to teach: "))
    
     #set the trainer's availiblity to this personal class session
     cur.execute("SELECT available FROM trainers WHERE trainer_id = %s", (user_input,))
     available=cur.fetchone()
     cur.execute("UPDATE group_classes SET time = (%s) WHERE group_classes_id = (%s);", 
              (available, user_input4))
     
     cur.execute("SELECT name FROM group_classes WHERE group_classes_id = %s", (user_input4,))
     groupClass=cur.fetchall()
     cur.execute("SELECT first_name FROM trainers WHERE trainer_id = %s", (user_input,))
     trainer_name=cur.fetchall()
      
     print("Congrats ", trainer_name, "! You're teaching class: ", groupClass)
     

def getExercisesByID(exercise_id):
     cur.execute("SELECT * FROM exercises WHERE exercises_id = (%s);",
                    (exercise_id,))
     exercises = cur.fetchall()
     for exercise in exercises:
        print(exercise)

     print("\nExecercise ID:", exercise[0])
     print("----------------------------------")
     print("Name: ", exercise[1])
     print("Number of Sets: ", exercise[2])
     print("Description: ", exercise[3])
     print("Muscle Group: ", exercise[4])
     print("Difficulty Level: ", exercise[5])
     print("Duration: ", exercise[6], ' minutes')

def getAllExercises():
     cur.execute("SELECT * FROM exercises")
     exercises = cur.fetchall()
     print("Exercise Routines:")
     for exercise in exercises:
         print(exercise)

def getHealthbyID(member):
     cur.execute("SELECT * FROM health_statistics WHERE member_id = (%s);",
                    (member,))
     health_stats = cur.fetchall()
     for health_stat in health_stats:
        print(health_stat)

     print("\nHealth Statistics:", health_stat[0])
     print("----------------------------------")
     print("Member ID: ", health_stat[1])
     print("Weight: ", health_stat[2], ' lbs')
     print("Height: ", health_stat[3], 'feet')
     print("BMI: ", health_stat[4])
     print("Resting Heart rate: ", health_stat[5], ' BPM')

def dashboard():                
     member=getMemberbyID()
     print("\n ----------- Member ------------")
     print("\n|  1. View Member Information   |")
     print("\n|  2. Update Member Information |")
     print("\n|  3. Exercise Routines         |")
     print("\n|  4. Fitness Achievements      |")
     user_input=int(input("\nPick an option from the Dashboard: "))
     if user_input==1:
        getMemberInfo()
     elif user_input==2:
        update_member_info()
     elif user_input==3:
        getAllExercises()
        user_input2=int(input("Select a workout for details"))
        getExercisesByID(user_input2)
     elif user_input==4:
        getHealthbyID(member)

def lookup_member():
    print("Search the member that you want to lookup: ")
    first_name = input(print("Enter the first name of the member: "))
    last_name = input(print("Enter the last name of the member: "))
    
    cur.execute("SELECT * FROM members WHERE first_name = %s AND last_name = %s", (first_name, last_name))
    searched_member = cur.fetchone()

    if searched_member:
        print("Member found:")
        print("Member ID: ", searched_member[0])
        print("First Name: ", searched_member[1])
        print("Last Name: ", searched_member[2])
        print("Height: ", searched_member[6])
        print("Fitness goal: ", searched_member[5])
        print ("Weight: ", searched_member[4])
        print("Date to achieve: ", searched_member[3])
    else:
        print("Member not found.")

def monitor_equipment_maintenance():
    print("EQUIPMENT MAINTENANCE MONITORING")
    print("---------------------------------")
    print("1. View Equipment Maintenance Status")
    print("2. Update Equipment Maintenance Status")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        # View equipment maintenance status
        cur.execute("SELECT * FROM equipments")
        equipments = cur.fetchall()
        if equipments:
            print("Equipment Maintenance Status:")
            for equipment in equipments:
                print("Equipment ID:", equipment[0])
                print("Equipment Name:", equipment[1])
                print("Counter:", equipment[2])
                print("--------------------------")
        else:
            print("No equipment records found.")
    elif choice == "2":
        # Update equipment maintenance status
        equipment_id = input("Enter Equipment ID: ")
        maintenance_counter = int(input("Enter Maintenance Counter: "))
        cur.execute("UPDATE equipments SET counter = %s WHERE equipments_id = %s",
                       (maintenance_counter, equipment_id))
        conn.commit()
        print("Equipment maintenance counter updated successfully.")
    else:
        print("Invalid choice. Please enter 1 or 2.")

def room_booking_management():
    print("ROOM BOOKING MANAGEMENT")
    print("-----------------------")
    print("1. View Room Bookings")
    print("2. Add Room Booking")
    print("3. Update Room Booking")
    print("4. Delete Room Booking")
    choice = input("Enter your choice (1, 2, 3, or 4): ")

    if choice == "1":
        # View room bookings
        cursor.execute("SELECT * FROM room")
        rooms = cursor.fetchall()
        if rooms:
            print("Rooms:")
            for room in rooms:
                print("Room ID:", room[0])
                print("Status:", room[1])
                print("Room Number:", room[2])
                print("--------------------------")
        else:
            print("No rooms found.")
    elif choice == "2":
        # Add room booking
        status = input("Enter Room Status: ")
        room_number = int(input("Enter Room Number: "))
        cursor.execute("INSERT INTO room (status, room_number) VALUES (%s, %s)",
                       (status, room_number))
        conn.commit()
        print("Room added successfully.")
    elif choice == "3":
        # Update room booking
        room_id = input("Enter Room ID to update: ")
        status = input("Enter New Room Status: ")
        room_number = int(input("Enter New Room Number: "))
        cursor.execute("UPDATE room SET status = %s, room_number = %s WHERE room_id = %s",
                       (status, room_number, room_id))
        conn.commit()
        print("Room updated successfully.")
    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

#-------------------------------------------------------------------------------------------------------------------
#Payment stuff

