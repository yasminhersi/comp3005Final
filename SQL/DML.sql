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

CREATE TABLE classes (
    classes_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    duration INTEGER,
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
CREATE TABLE staff (
    staff_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    available DATE	
);
