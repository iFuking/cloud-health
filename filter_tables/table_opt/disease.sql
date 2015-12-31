CREATE TABLE `disease` (
	`disease_id` INT(11) UNSIGNED NOT NULL, 
	`name` TEXT DEFAULT NULL, 
	`department` TEXT DEFAULT NULL, 
	`keywords` TEXT DEFAULT NULL, 
	`weight` TEXT DEFAULT NULL, 
	`content` LONGTEXT DEFAULT NULL, 
	PRIMARY KEY (`disease_id`)
) CHARACTER SET = 'UTF8';
