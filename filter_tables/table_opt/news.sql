CREATE TABLE `news` (
	`news_id` INT(11) UNSIGNED NOT NULL, 
	`title` TEXT DEFAULT NULL, 
	`tag` TEXT DEFAULT NULL, 
	`keywords` TEXT DEFAULT NULL, 
	`weight` TEXT DEFAULT NULL, 
	`content` LONGTEXT DEFAULT NULL, 
	PRIMARY KEY (`news_id`)
) CHARACTER SET = 'UTF8';
