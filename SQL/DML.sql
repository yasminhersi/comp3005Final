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
    number_sets INTEGER
);

