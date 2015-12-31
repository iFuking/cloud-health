CREATE TABLE `surgery` (
	`surgery_id` INT(11) UNSIGNED NOT NULL, 
	`name` TEXT DEFAULT NULL, 
	`department` TEXT DEFAULT NULL, 
	`keywords` TEXT DEFAULT NULL, 
	`weight` TEXT DEFAULT NULL, 
	`content` LONGTEXT DEFAULT NULL, 
	PRIMARY KEY (`surgery_id`)
) CHARACTER SET = `UTF8`;
