CREATE TABLE `administrator` (
  `admin_id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_name` varchar(100) NOT NULL,
  PRIMARY KEY (`admin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `calendar` (
  `reservation_date` date NOT NULL,
  `reservation_time` time NOT NULL,
  PRIMARY KEY (`reservation_date`,`reservation_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `members` (
  `car_plate_no` varchar(20) NOT NULL,
  `temp_plate_no` varchar(45) DEFAULT NULL,
  `member_id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  PRIMARY KEY (`member_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `non_member` (
  `non_member_id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  PRIMARY KEY (`non_member_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `parking_spot` (
  `lot_no` int(11) NOT NULL,
  `spot_no` int(11) NOT NULL,
  `building_name` varchar(100) NOT NULL,
  PRIMARY KEY (`lot_no`,`spot_no`,`building_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `reservation` (
  `reservation_id` int(11) NOT NULL AUTO_INCREMENT,
  `member_id` int(11) DEFAULT NULL,
  `non_member_id` int(11) DEFAULT NULL,
  `reservation_date` date NOT NULL,
  `reservation_time` time NOT NULL,
  `building_name` varchar(45) NOT NULL,
  `spot_no` varchar(45) NOT NULL,
  `lot_no` varchar(45) NOT NULL,
  PRIMARY KEY (`reservation_id`),
  KEY `member_id_idx` (`member_id`),
  KEY `non_member_id_idx` (`non_member_id`),
  KEY `date_idx` (`reservation_date`),
  KEY `time_idx` (`reservation_time`),
  KEY `building_name_idx` (`building_name`),
  KEY `spot_no_idx` (`spot_no`),
  KEY `lot_no_idx` (`lot_no`),
  CONSTRAINT `member_id` FOREIGN KEY (`member_id`) REFERENCES `members` (`member_id`),
  CONSTRAINT `non_member_id` FOREIGN KEY (`non_member_id`) REFERENCES `non_member` (`non_member_id`),
  CONSTRAINT `reservation_date` FOREIGN KEY (`reservation_date`) REFERENCES `calendar` (`reservation_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `staff` (
  `staff_id` int(11) NOT NULL AUTO_INCREMENT,
  `staff_name` varchar(100) NOT NULL,
  PRIMARY KEY (`staff_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `login` (
  `member_id` int(11),
  `non_member_id` int(11),
  `login_time` DATETIME NOT NULL,
  `logout_time` DATETIME NOT NULL,
  PRIMARY KEY (`member_id`, `non_member_id`, `login_time`, `logout_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;