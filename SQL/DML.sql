CREATE TABLE members (
    member_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    achieved_date DATE,
    curr_weight INTEGER,
    #used to be goal_weight
    fitness_goal VARCHAR(255) NOT NULL, 
    height INTEGER,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
CREATE TABLE trainers (
    trainers_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    available TIMESTAMP
);
CREATE TABLE staff (
    staff_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    available TIMESTAMP
);

CREATE TABLE group_classes (
    group_classes_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    duration INTEGER,
    time TIMESTAMP,
    trainer_id INT,
    members_count INT,
    max_members INT,
    FOREIGN KEY (trainer_id) REFERENCES trainers(trainer_id)
);

CREATE TABLE personal_classes (
     personal_classes_id SERIAL PRIMARY KEY,
     name VARCHAR(255) NOT NULL,
     duration INTEGER,
     available TIMESTAMP,
     trainer_id INTEGER,
     member_id INTEGER,
     FOREIGN KEY (member_id) REFERENCES members(member_id),
     FOREIGN KEY (trainer_id) REFERENCES trainers(trainer_id)
);
CREATE TABLE equipments (
    equipments_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    counter INTEGER 
);
CREATE TABLE exercises (
    exercises_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sets INTEGER,
	description TEXT,
	muscle_group VARCHAR(255) NOT NULL,
	difficulty_level INTEGER,
	minutes INTEGER
);
CREATE TABLE health_statistics (
    health_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL,
    weight INTEGER,
	height VARCHAR(255) NOT NULL,
	BMI INTEGER,
	resting_heart INTEGER,
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);
#create a room bookings table
CREATE TABLE room (
    room_id SERIAL PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    room_number INTEGER,
);
