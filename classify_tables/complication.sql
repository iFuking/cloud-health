CREATE TABLE `complication` (
	`id` INT(11) NOT NULL, 
	`complications` TEXT DEFAULT NULL, 
	PRIMARY KEY (`id`)
) CHARACTER SET = 'UTF8';

/*
INSERT INTO complication(id, complications) VALUES(1, '3,4,5,6,');
INSERT INTO complication(id, complications) VALUES(2, '1,7,8,9,10,11,12,');
*/
