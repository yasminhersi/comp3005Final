CREATE TABLE members (
    member_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    achieved_date DATE,
    curr_weight INTEGER,
    goal_weight INTEGER,
    height INTEGER
);
CREATE TABLE trainers (
    trainer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    available DATE
);
CREATE TABLE staff (
    staff_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    available DATE
);

CREATE TABLE group_classes (
    classes_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    duration INTEGER,
    available DATE,
    trainer_id INT,
    FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id),

);
CREATE TABLE personal_classes (
     personal_classes_id SERIAL PRIMARY KEY,
     name VARCHAR(255) NOT NULL,
   	 duartion INTEGER,
     available DATE
);
CREATE TABLE equipments (
    equipment_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    counter INTEGER 
);
CREATE TABLE exercises (
    exercises_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    number_sets INTEGER
);

