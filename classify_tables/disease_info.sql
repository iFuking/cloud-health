CREATE TABLE `disease_info` (
	`disease_id` INT(11) NOT NULL AUTO_INCREMENT, 
	`name` VARCHAR(255) DEFAULT NULL, 
	`ask` TEXT DEFAULT NULL, 
	`book` TEXT DEFAULT NULL, 
	`checks` TEXT DEFAULT NULL, 
	`disease` TEXT DEFAULT NULL, 
	`drug` TEXT DEFAULT NULL, 
	`food` TEXT DEFAULT NULL, 
	`lore` TEXT DEFAULT NULL, 
	`news` TEXT DEFAULT NULL, 
	`surgery` TEXT DEFAULT NULL, 
	`symptom` TEXT DEFAULT NULL, 
	PRIMARY KEY (`disease_id`), 
	UNIQUE KEY `name` (`name`)
) CHARACTER SET = 'UTF8';
