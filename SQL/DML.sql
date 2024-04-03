CREATE TABLE members (
    member_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
  	achieved_date DATE
  	weight NUMBER
  	height NUMBER
  	goal_weight NUMBER	
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
