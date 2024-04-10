INSERT INTO members (member_id, first_name, last_name, achieved_date, curr_weight, fitness_goal, height, username, password)
VALUES 
(1, 'John', 'Doe', '2024-05-01', 150, 170, 'to be ...', 'yasmin', '123'),
(2, 'Smith', 'jane', '2024-08-01', 120, 150, 'to be ....', 'fatima', '123');

INSERT INTO personal_classes (personal_classes_id, name, duration, available, trainer_id)
VALUES 
(1, 'HIIT', 30, '2024-04-12', NULL),
(2, 'Cardio', 45, '2024-04-13', NULL);

INSERT INTO group_classes (group_classes_id, name, duration, time, trainer_id, members_count, max_members)
VALUES 
(1, 'Pilates', 30, '2024-04-10 16:00:00', NULL, NULL, 4),
(2, 'Spinning', 45, '2024-04-10 19:00:00', NULL, NULL, 3);
