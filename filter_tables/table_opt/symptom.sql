CREATE TABLE `symptom` (
	`symptom_id` INT(11) UNSIGNED NOT NULL, 
	`name` TEXT DEFAULT NULL, 
	`place` TEXT DEFAULT NULL, 
	`keywords` TEXT DEFAULT NULL, 
	`weight` TEXT DEFAULT NULL, 
	`content` LONGTEXT DEFAULT NULL, 
	PRIMARY KEY (`symptom_id`)
) CHARACTER SET = 'UTF8';
