INSERT INTO members (member_id, first_name, last_name, achieved_date, fitness_goal,  curr_weight, height, username, password)
VALUES 
(1, 'John', 'Doe', '2024-05-01',  'to loose 10 lbs of fat', 150, 170, 'yasmin', '123'),
(2, 'Smith', 'jane', '2024-08-01', 'to gain 10 lbs of muscle', 120, 150, 'fatima', '123');


INSERT INTO personal_classes (personal_classes_id, name, duration, available, trainer_id, member_id, price)
VALUES 
(1, 'HIIT', 30, '2024-04-08 10:00:00', NULL, NULL, 20),
(2, 'Cardio', 45, '2024-04-18 12:00:00', NULL, NULL, 10);

INSERT INTO group_classes (group_classes_id, name, duration, time, trainer_id, members_count, max_members, price)
VALUES 
(1, 'Pilates', 30, '2024-04-10 16:00:00', NULL, NULL, 4, 5),
(2, 'Spinning', 45, '2024-04-10 19:00:00', NULL, NULL, 3, 8);

INSERT INTO exercises (exercises_id, name, sets, description, muscle_group, difficulty_level, minutes)
VALUES
(1, 'Plank', 2, 'Keep forearms and toes on ground and lift up', 'abs', 5, 2),
(2, 'Squat', 10, 'Spread legs and bend knees with back straight', 'legs', 8, 3),
(3, 'Jumping Jacks', 15, 'Jump while spreading arms and legs', 'legs and arms', 2, 5);

INSERT INTO health_statistics (health_id, member_id, weight, height, BMI, resting_heart)
VALUES
(1, 1, 150, '5 1', 20, 90),
(2, 2, 130, '5 7', 22, 70);

INSERT INTO room (room_id, status, room_number)
VALUES
(1, 'FREE', 1),
(2, 'FREE', 2);
