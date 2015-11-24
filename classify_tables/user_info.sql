CREATE TABLE `user_info` (
	`open_id` VARCHAR(255) NOT NULL, 
	`disease_id` TEXT DEFAULT NULL, 
	`complications` TEXT DEFAULT NULL, 
	PRIMARY KEY (`open_id`)
) CHARACTER SET = 'UTF8';
