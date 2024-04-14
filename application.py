import psycopg2
import string

# Connect to your postgres DB
conn = psycopg2.connect("dbname=comp3005 user=postgres password=student host=localhost port=5432")

# Open a cursor to perform database operations
cur = conn.cursor()

#Retrieves and displays all records from the students table.
def getAllMembers(): 
    # Execute a query
    cur.execute("SELECT * FROM members")
    # Retrieve query results
    members = cur.fetchall()
    #print each row of students
    for member in members:
        print(member)


def getMemberbyID():     
        memberUser  = input("\nEnter member username: ")
        memberPass = input("Enter member password: ")
        cur.execute("SELECT member_id FROM members WHERE username = (%s) AND password = (%s) ;", 
                    (memberUser, memberPass))

        member_id = cur.fetchone()
        
        if member_id:
            print("Member ID found:", member_id)
            return member_id
        else:
            print("Member not found.")
            exit(1)
        
def login():
    memberUser = input("Enter member username: ")
    memberPass = input("Enter member password: ")
    cur.execute("SELECT * FROM members WHERE username = (%s) AND password = (%s) ;", 
        (memberUser, memberPass))
    member = cur.fetchone()
    if member:
        print("Member found:", member)
        return member
    else:
        print("Member not found.")  
        exit(1)

def getMemberInfo(member_id):
        cur.execute("SELECT * FROM members WHERE member_id = (%s) ;", 
        (member_id,))
        member = cur.fetchone()
        if member:
            print("\nMember ID:", member[0])
            print("\nHEALTH METRICS")
            print("--------------------------------------------------------------------------------------------")
            print("Name: ", member[1], " ", member[2])
            print("Height: ", member[7], " cm")
            print("Weight: ", member[5], " lbs")
            print("Goal: ", member[6], " lbs")
            print("Want to achieve this goal by: ", member[4])
        else:
            print("Member not found.")

#getting this to work with the other function with proper sequence
def update_member_info():
    user_input = input("Would you like to update your information? (Y | N): ")

    while True:
        if user_input == "Y":
            print("Please enter the following information to update your profile:")
            fitness_goal = input("New Fitness Goal: ")
            weight = int(input("New Weight (lbs): "))
            height = int(input("New Height (cm): "))
            achieved_date = input("New date to achieve by: ")
            cur.execute("UPDATE members SET fitness_goal = %s, curr_weight = %s, height = %s, achieved_date = %s",
                    (fitness_goal, weight, height, achieved_date))
            print("\nPersonal information has been updated!")
            
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
    fitness_goal = input("Fitness Goal: ")
    achievement_date = input("Please insert the date you would like to achieve your fitness goal by (year-month-day): ")

    cur.execute("SELECT MAX(member_id) FROM members")
    max_id = cur.fetchone()[0]
    if max_id is None:
        member_id = 1
    else:
        member_id = max_id + 1

    cur.execute("INSERT INTO members (member_id, first_name, last_name, achieved_date, fitness_goal, curr_weight, height, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (member_id, first_name, last_name, achievement_date, fitness_goal, weight, height, username, password))
    getAllMembers()
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

# Function to generate invoice
def generate_invoice(member_id, amount_due):
    cur.execute("INSERT INTO invoice (member_id, amount_due) VALUES (%s, %s)",
                   (member_id, amount_due))
    conn.commit()
    print("Class costs: $", amount_due)
    print("Invoice generated successfully.")

# Function to process payment (Member version)
def process_payment_member(invoice_id, payment_amount):
    cur.execute("INSERT INTO payment (invoice_id, amount_due) VALUES (%s, %s)",
                   (invoice_id, payment_amount))
    conn.commit()
    print("Payment of $",  payment_amount, " processed successfully.")

#this function is for members to pick a group or personal class, then register in one that interests them. Classes are displayed
def registerClass(member_by_id):
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

                cur.execute("SELECT price FROM personal_classes WHERE personal_classes_id = (%s) ;", 
                    (personal_class_id))
                amount_due=cur.fetchone()
                generate_invoice(member_by_id, amount_due)
                
                paymentPromp=input("Would you like to proceed with payment? (Y OR N): ")
                if(paymentPromp=='Y'):
                    cur.execute("SELECT invoice_id FROM invoice WHERE member_id = (%s) ;", 
                                    (member_by_id,))
                    invoice_id=cur.fetchone()
                    process_payment_member(invoice_id, amount_due)
                    cur.execute("UPDATE personal_classes SET member_id= (%s) WHERE personal_classes_id = (%s);", 
                                    (member_by_id, personal_class_id))
                    print("Registered!")
                else:
                    print("Payment cancelled")
                    return
                     
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
                
                cur.execute("SELECT price FROM group_classes WHERE group_classes_id = (%s) ;", 
                (group_class_id))
                amount_due=cur.fetchone()
                generate_invoice(member_by_id, amount_due)
                
                paymentPromp=input("Would you like to proceed with payment? (Y OR N): ")
                if(paymentPromp=='Y'):
                    cur.execute("SELECT invoice_id FROM invoice WHERE member_id = (%s) ;", 
                                (member_by_id,))
                    invoice_id=cur.fetchone()
                    process_payment_member(invoice_id, amount_due)
                else:
                    print("Payment cancelled")
                    return
                cur.execute("UPDATE group_classes SET members_count = (%s) WHERE group_classes_id = (%s);", 
                                  (members_count, group_class_id))
                cur.execute("SELECT max_members FROM group_classes WHERE group_classes_id = (%s);",
                                   (group_class_id,))
                #find max members value for current group class id and check if capacity has reached before registering
                max_members=cur.fetchone()[0]
                print("max members:", max_members)
                print("member count:", members_count)
                if members_count<max_members :
                    cur.execute("UPDATE group_classes SET member_id= (%s) WHERE group_classes_id = (%s);", 
                                    (member_by_id, group_class_id))
                    print("You've successfully registered for this class")
                else:
                    print("Sorry class is full :(")
            else:
                print("Group class ID not found.")
        else:
            print("Enter a correct option")

def lookup_member():
    print("Search the member that you want to lookup: ")
    first_name = input("Enter the first name of the member: ")
    last_name = input("Enter the last name of the member: ")
    
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

def scheduleTrainer():
  getAllTrainers()
  user_input=int(input("Which Trainer ID are you: "))
  
  #lookup member
  pick=input("Would you like to look up a member? (Y OR N)")
  if pick == "Y":
      lookup_member()
  else:
      print("Got it!")
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
     
  print("Congrats! You're teaching class: ")

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
     print("BMI: ", health_stat[2])
     print("Resting Heart rate: ", health_stat[3], ' BPM')
def deleteClass(member_id):
    user_in=int(input("Would you like to delete a personal (1) or group class (2)?\n"))
    if user_in==1:
        cur.execute("SELECT * FROM personal_classes WHERE member_id = (%s);", 
                    (member_id))
        personalClass=cur.fetchall()
        cur.execute("DELETE FROM personal_classes WHERE member_id = (%s);", 
                    (member_id))
        print("DONE! You deleted your personal class\n", personalClass)
    elif user_in==2:
        cur.execute("SELECT * FROM group_classes WHERE member_id = (%s);", 
                    (member_id))
        groupClass=cur.fetchall()
        cur.execute("DELETE FROM group_classes WHERE member_id = (%s);", 
                    (member_id))
        print("DONE! You deleted your group class\n", groupClass)
    else:
        print("Enter a correct option")

def rescheduleClass(member):
    print("Must register for a class before rescheduling one")
    registerClass(member)
    user_input=int(input("Would you like to reschedule a personal (1) or group class (2)\n"))
    if user_input==1:
        getAllPersonalClasses()

        class_id=int(input("Enter which class ID to update"))
        cur.execute("SELECT * FROM personal_classes WHERE personal_classes_id = (%s)", 
                        (class_id,))
        personal_class=cur.fetchall()
        print("You picked class: ", personal_class)
        #2024-04-10 16:00:00
        newTime=input("Update schedule to what date and time (using format yyyy-mm-dd hh:mm:ss): ")
        cur.execute("UPDATE personal_classes SET available = (%s) WHERE personal_classes_id = (%s);", 
            (newTime, class_id))
        cur.execute("SELECT * FROM personal_classes WHERE personal_classes_id = (%s)", 
                        (class_id,))
        personal_class=cur.fetchall()
        print("Class updated: ", personal_class)
    elif user_input==2:
        class_id=int(input("Enter which class ID to update"))
        cur.execute("SELECT * FROM group_classes WHERE group_classes_id = (%s)", 
                        (class_id,))
        group_class=cur.fetchall()
        print("You picked class: ", group_class)
        #2024-04-10 16:00:00
        newTime=input("Update schedule to what(using format yyyy-mm-dd hh:mm:ss): ")
        cur.execute("UPDATE group_classes SET time = (%s) WHERE group_classes_id = (%s);", 
            (newTime, class_id))
        cur.execute("SELECT * FROM group_classes WHERE group_classes_id = (%s)", 
                        (class_id,))
        group_class=cur.fetchall()
        print("Class updated: ", group_class)


def dashboard():                
     member=getMemberbyID()
     print("\n ----------- Member ------------")
     print("\n|  1. View Member Information   |")
     print("\n|  2. Update Member Information |")
     print("\n|  3. Exercise Routines         |")
     print("\n|  4. Fitness Achievements      |")
     print("\n|  5. Register For a Class      |")
     print("\n|  6. Delete an Upcoming Class  |")
     print("\n|  7. Reschedule a Class        |")
     user_input=int(input("\nPick an option from the Dashboard: "))
     if user_input==1:
        getMemberInfo(member)
     elif user_input==2:
        update_member_info()
        getMemberInfo(member)
     elif user_input==3:
        getAllExercises()
        user_input2=int(input("Select a workout for details"))
        getExercisesByID(user_input2)
     elif user_input==4:
        getHealthbyID(member)
     elif user_input==5:
        registerClass(member)
     elif user_input==6:
        deleteClass(member)
     elif user_input==7:
         rescheduleClass(member)

def loginStaff():
    staffUser = input("Enter STAFF username: ")
    staffPass = input("Enter STAFF password: ")
    cur.execute("SELECT * FROM staff WHERE username = (%s) AND password = (%s) ;", 
        (staffUser, staffPass))
    staff = cur.fetchone()
    if staff:
        print("STAFF found:", staff)
        return staff
    else:
        print("STAFF not found.") 
        exit(1)

def updatePersonalClassSchedule():
        getAllPersonalClasses()
         
        class_id=int(input("Enter which class ID to update"))
        cur.execute("SELECT * FROM personal_classes WHERE personal_classes_id = (%s)", 
                        (class_id,))
        personal_class=cur.fetchall()
        print("You picked class: ", personal_class)
        #2024-04-10 16:00:00
        newTime=input("Update schedule to what date and time (using format yyyy-mm-dd hh:mm:ss): ")
        cur.execute("UPDATE personal_classes SET available = (%s) WHERE personal_classes_id = (%s);", 
            (newTime, class_id))
        cur.execute("SELECT * FROM personal_classes WHERE personal_classes_id = (%s)", 
                        (class_id,))
        personal_class=cur.fetchall()
        print("Class updated: ", personal_class)
   
def updateGroupClassSchedule():
        getAllGroupClasses()
        class_id=int(input("Enter which class ID to update"))
        cur.execute("SELECT * FROM group_classes WHERE group_classes_id = (%s)", 
                        (class_id,))
        group_class=cur.fetchall()
        print("You picked class: ", group_class)
        #2024-04-10 16:00:00
        newTime=input("Update schedule to what(using format yyyy-mm-dd hh:mm:ss): ")
        cur.execute("UPDATE group_classes SET time = (%s) WHERE group_classes_id = (%s);", 
            (newTime, class_id))
        cur.execute("SELECT * FROM group_classes WHERE group_classes_id = (%s)", 
                        (class_id,))
        group_class=cur.fetchall()
        print("Class updated: ", group_class)

def overseeBillings():
    cur.execute("SELECT * FROM payment")
    payments = cur.fetchall()
    print("\nPayments\n")
    for payment in payments:
        print(payment)


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
            print("Equipment Maintenance Information:")
            for equipment in equipments:
                print("Equipment ID:", equipment[0])
                print("Equipment Name:", equipment[1])
                print("status:", equipment[2])
                print("--------------------------")
        else:
            print("No equipment records found.")
    elif choice == "2":
        # Update equipment maintenance status
        equipment_id = input("Enter Equipment ID: ")
        maintenance_status = input("Enter Maintenance: ")
        cur.execute("UPDATE equipments SET status = %s WHERE equipment_id = %s",
                       (maintenance_status, equipment_id))
        conn.commit()
        print("Equipment maintenance status updated successfully.")
    else:
        print("Invalid choice. Please enter 1 or 2.")

def room_booking_management():
    print("ROOM BOOKING MANAGEMENT")
    print("-----------------------")
    print("1. View Room Bookings")
    print("2. Add Room Booking")
    print("3. Update Room Booking")
    choice = input("Enter your choice (1, 2, 3): ")

    if choice == "1":
        # View room bookings
        cur.execute("SELECT * FROM room")
        rooms = cur.fetchall()
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
        cur.execute("SELECT MAX(room_id) FROM room")
        max_id = cur.fetchone()[0]
        if max_id is None:
            room_id = 1
        else:
            room_id = max_id + 1
        
        cur.execute("INSERT INTO room (room_id, status, room_number) VALUES (%s, %s, %s)",
                       (room_id, status, room_number,))
        conn.commit()
        print("Room added successfully.")
    elif choice == "3":
        # Update room booking
        room_id = input("Enter Room ID to update: ")
        status = input("Enter New Room Status: ")
        room_number = int(input("Enter New Room Number: "))
        cur.execute("UPDATE room SET status = %s, room_number = %s WHERE room_id = %s",
                       (status, room_number, room_id))
        conn.commit()
        print("Room updated successfully.")
    else:
        print("Invalid choice. Please enter 1, 2, 3")

#Class Schedule Updating
def staffManagment():
     loginStaff()
     #update class schedules
     print("\n --------------- STAFF ---------------")
     print("\n|  1. Update Personal Class Schedules |")
     print("\n|  2. Update Group Class Schedules    |")
     print("\n|  3. Oversee Billings and Payments   |")
     print("\n|  4. Monitor Room Bookings           |")
     print("\n|  5. Monitor Fitness Equipement      |")
     print("\n|  6. Lookup Member Info              |")
     user_input=int(input("Hi STAFF, pick an option from above: "))
     if(user_input==1):
            updatePersonalClassSchedule()
     elif(user_input==2):
            updateGroupClassSchedule()
     elif(user_input==3):
            overseeBillings()
     elif(user_input==4):
            room_booking_management()
     elif(user_input==5):
            monitor_equipment_maintenance()
     elif(user_input==6):
            lookup_member()
     else:
         print("Enter a correct option")
         
pick=input("Are you a newcomer, member, trainer or staff?\n")
if(pick=="newcomer"):
    register_member()
elif(pick=="member"):
    dashboard()
elif (pick == "trainer"):
    scheduleTrainer()
elif (pick == "staff"):
    staffManagment()
else:
    print("Enter a correct option")
    
