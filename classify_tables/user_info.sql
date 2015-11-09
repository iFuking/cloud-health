CREATE TABLE `user_info` (
	`id` BINARY(16) NOT NULL, 
	`disease_id` TEXT DEFAULT NULL, 
	`complications` TEXT DEFAULT NULL, 
	PRIMARY KEY (`id`)
) CHARACTER SET = 'UTF8';
