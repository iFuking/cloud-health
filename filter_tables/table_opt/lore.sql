CREATE TABLE `lore` (
	`lore_id` INT(11) UNSIGNED NOT NULL, 
	`title` TEXT DEFAULT NULL, 
	`classname` TEXT DEFAULT NULL, 
	`keywords` TEXT DEFAULT NULL, 
	`weight` TEXT DEFAULT NULL, 
	`content` LONGTEXT DEFAULT NULL, 
	PRIMARY KEY (`lore_id`)
) CHARACTER SET = 'UTF8';