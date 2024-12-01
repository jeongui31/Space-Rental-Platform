-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: dbdesign
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking` (
  `booking_id` int NOT NULL AUTO_INCREMENT,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `booking_status` enum('Pending','Confirmed','Canceled') NOT NULL,
  `booking_created_at` datetime(6) NOT NULL,
  `booking_updated_at` datetime(6) NOT NULL,
  `space_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`booking_id`),
  KEY `booking_space_id_8b2a5487_fk_space_space_id` (`space_id`),
  KEY `booking_user_id_1bd7cb6e_fk_User_user_id` (`user_id`),
  CONSTRAINT `booking_space_id_8b2a5487_fk_space_space_id` FOREIGN KEY (`space_id`) REFERENCES `space` (`space_id`),
  CONSTRAINT `booking_user_id_1bd7cb6e_fk_User_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `check_end_date_gte_start_date` CHECK ((`end_date` >= `start_date`))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking`
--

LOCK TABLES `booking` WRITE;
/*!40000 ALTER TABLE `booking` DISABLE KEYS */;
INSERT INTO `booking` VALUES (1,'2024-12-01','2024-12-03','Confirmed','2024-12-01 04:23:54.882878','2024-12-01 04:27:03.926898',2,3),(2,'2024-12-08','2024-12-08','Confirmed','2024-12-01 04:24:05.788572','2024-12-01 04:27:05.949264',4,3),(3,'2024-12-14','2024-12-14','Confirmed','2024-12-01 04:24:38.408577','2024-12-01 04:27:08.614950',4,4),(4,'2024-12-06','2024-12-07','Confirmed','2024-12-01 04:24:59.880611','2024-12-01 04:27:01.471809',1,5),(5,'2024-12-15','2024-12-16','Confirmed','2024-12-01 04:25:13.991633','2024-12-01 04:26:58.277349',5,5),(6,'2024-12-15','2024-12-15','Confirmed','2024-12-01 04:25:26.353141','2024-12-01 04:26:55.026308',3,5),(7,'2024-12-13','2024-12-14','Confirmed','2024-12-01 04:25:49.827535','2024-12-01 04:26:52.570788',1,6),(8,'2024-12-21','2024-12-22','Confirmed','2024-12-01 04:26:03.057722','2024-12-01 04:26:50.357860',2,6),(9,'2024-12-18','2024-12-20','Confirmed','2024-12-01 04:26:17.167962','2024-12-01 04:26:48.220788',3,6),(10,'2024-12-16','2024-12-17','Confirmed','2024-12-01 04:26:25.352753','2024-12-01 04:26:46.564786',4,6),(11,'2024-12-29','2024-12-30','Confirmed','2024-12-01 04:26:34.018069','2024-12-01 04:26:45.031797',5,6),(12,'2024-12-18','2024-12-18','Confirmed','2024-12-01 04:41:07.098146','2024-12-01 04:41:49.757371',5,4);
/*!40000 ALTER TABLE `booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `host`
--

DROP TABLE IF EXISTS `host`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `host` (
  `user_id` int NOT NULL,
  `company_name` varchar(100) DEFAULT NULL,
  `business_license` varchar(30) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `business_license` (`business_license`),
  CONSTRAINT `host_user_id_b7bd01e7_fk_User_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `host`
--

LOCK TABLES `host` WRITE;
/*!40000 ALTER TABLE `host` DISABLE KEYS */;
INSERT INTO `host` VALUES (1,'김동국','111'),(2,'이명진','1234');
/*!40000 ALTER TABLE `host` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `payment_id` int NOT NULL AUTO_INCREMENT,
  `amount` int unsigned NOT NULL,
  `payment_method` enum('Credit Card','Debit Card','Bank Transfer','Mobile Payment') NOT NULL,
  `payment_status` enum('Success','Failed') NOT NULL,
  `payment_created_at` datetime(6) NOT NULL,
  `booking_id` int NOT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `payment_booking_id_d8426f2f_fk_booking_booking_id` (`booking_id`),
  CONSTRAINT `payment_booking_id_d8426f2f_fk_booking_booking_id` FOREIGN KEY (`booking_id`) REFERENCES `booking` (`booking_id`),
  CONSTRAINT `payment_chk_1` CHECK ((`amount` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (1,510000,'Bank Transfer','Success','2024-12-01 04:23:54.883878',1),(2,990000,'Credit Card','Success','2024-12-01 04:24:05.789570',2),(3,990000,'Bank Transfer','Success','2024-12-01 04:24:38.408577',3),(4,400000,'Debit Card','Success','2024-12-01 04:24:59.881611',4),(5,300000,'Debit Card','Success','2024-12-01 04:25:13.991633',5),(6,500000,'Debit Card','Success','2024-12-01 04:25:26.354140',6),(7,400000,'Bank Transfer','Success','2024-12-01 04:25:49.828535',7),(8,340000,'Credit Card','Success','2024-12-01 04:26:03.058732',8),(9,1500000,'Bank Transfer','Success','2024-12-01 04:26:17.167962',9),(10,1980000,'Debit Card','Success','2024-12-01 04:26:25.353751',10),(11,300000,'Debit Card','Success','2024-12-01 04:26:34.018069',11),(12,150000,'Mobile Payment','Success','2024-12-01 04:41:07.099145',12);
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `review` (
  `review_id` int NOT NULL AUTO_INCREMENT,
  `review_rating` int unsigned NOT NULL,
  `comment` longtext,
  `review_created_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  `booking_id` int DEFAULT NULL,
  PRIMARY KEY (`review_id`),
  UNIQUE KEY `booking_id` (`booking_id`),
  KEY `review_user_id_1520d914` (`user_id`),
  CONSTRAINT `review_booking_id_e6694020_fk_booking_booking_id` FOREIGN KEY (`booking_id`) REFERENCES `booking` (`booking_id`),
  CONSTRAINT `review_user_id_1520d914_fk_User_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `check_review_rating_range` CHECK (((`review_rating` >= 1) and (`review_rating` <= 5))),
  CONSTRAINT `review_chk_1` CHECK ((`review_rating` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
INSERT INTO `review` VALUES (1,4,'공연장이 넓고 좋아요!','2024-12-01 04:42:20.704383',3,2),(2,3,'특별하진 않고 평범하네요','2024-12-01 04:43:08.091401',3,1),(3,5,'분위기가 제가 원하던 분위기였어요!','2024-12-01 04:43:39.865093',4,12),(4,2,'제가 원하던 느낌은 아니였네요...','2024-12-01 04:44:04.717494',4,3),(5,5,'최고에요!','2024-12-01 04:45:21.733494',5,5),(6,4,'무난합니다','2024-12-01 04:45:37.623905',5,6),(7,4,'촬용하기 좋았어요.','2024-12-01 04:46:04.003690',5,4),(8,2,'저는 좀 별로였네요','2024-12-01 04:46:32.679737',6,11),(9,5,'즐거운 연말 분위기를 느낄 수 있어요','2024-12-01 04:46:46.292756',6,8),(10,5,'시설이 잘 갖춰져 있어요','2024-12-01 04:47:41.480850',6,9),(11,4,'넓어서 좋았어요!','2024-12-01 04:48:10.663058',6,10),(12,1,'너무 아쉬운 부분이 많아요','2024-12-01 04:48:39.930644',6,7);
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `space`
--

DROP TABLE IF EXISTS `space`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `space` (
  `space_id` int NOT NULL AUTO_INCREMENT,
  `space_name` varchar(200) NOT NULL,
  `description` longtext,
  `address` varchar(200) NOT NULL,
  `capacity` int unsigned NOT NULL,
  `price_per_date` int unsigned NOT NULL,
  `space_created_at` datetime(6) NOT NULL,
  `space_updated_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  `image` text,
  PRIMARY KEY (`space_id`),
  KEY `space_user_id_1ea2c426_fk_User_user_id` (`user_id`),
  KEY `idx_space_name` (`space_name`),
  CONSTRAINT `space_user_id_1ea2c426_fk_User_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `space_chk_1` CHECK ((`capacity` >= 0)),
  CONSTRAINT `space_chk_2` CHECK ((`price_per_date` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `space`
--

LOCK TABLES `space` WRITE;
/*!40000 ALTER TABLE `space` DISABLE KEYS */;
INSERT INTO `space` VALUES (1,'아늑한 홈무드의 스튜디오','동향, 남향, 서향에서 풍부한 채광이 들어오는\r\n자연광 스튜디오로 아늑한 무드의 오래된 빈티지 가구들과 소파, 키친, 침대 파트, 호리존으로 활용할 수 있는 심플한 화이트 가벽 등으로 다양하고 감각적인 인테리어 파트가 구성 되어있습니다','서울특별시 용산구',10,200000,'2024-12-01 03:58:45.066136','2024-12-01 03:58:45.066136',1,'https://i.ibb.co/8DsDtJB/Q1-IHq1698385788.jpg'),(2,'유니크 크리스마스 스튜디오','뉴욕 아티스트의 소호 작업실을 테마로 꾸며진 5가지 컨셉의 스튜디오입니다. 25평의 공간을 단독 사용하며, 유튜브, 인터뷰, 노래 커버, 화보 촬영에 최적화된 렌탈 스튜디오입니다.','서울특별시 광진구',5,170000,'2024-12-01 04:02:44.090908','2024-12-01 04:02:44.090908',1,'https://i.ibb.co/RpY4fcm/5624daf96f39c.jpg'),(3,'조리 가능한 식당 스튜디오','방송 또는 상업광고 촬영, 팝업 전시 등은 별도 문의 부탁드립니다.   [촬영 장소로의 장점] 카페나 음식점 컨셉으로 촬영 하실 수 있고 요리나 커피 컨텐츠 등에 적합합니다. 매장 옆 주차가 용이하고 탑차도 주차 가능합니다. \r\n1층에 주차가 편하게 되어 짐을 이동하기 편하다는 점  차량으로 오시면 강남 및 양재 , 경기등에서도 오시기 편한 위치에 있다는 점이 장점입니다 .','경기도 파주시 ',20,500000,'2024-12-01 04:07:19.182030','2024-12-01 04:07:19.182030',1,'https://i.ibb.co/ct3kML9/1.jpg'),(4,'300석 규모의 공연장/강의장/회의장','300석 규모의 공연/강연/회의 등이 가능한 복합 문화 공간입니다.\r\n행사 규모에 따라 내부 배치는 가변적으로 세팅이 가능 합니다.\r\n상업시설내 위치하여 주변 편의 시설 이용이 편리 합니다.','경기도 성남시',300,990000,'2024-12-01 04:10:10.946059','2024-12-01 04:10:10.946059',2,'https://i.ibb.co/CB06RmQ/open-space.png'),(5,'분위기 좋은 자연광 렌탈 스튜디오','은은한 서향 채광의 편안하고 자연스러운 분위기를 가진 공간입니다. 꽃 그리고 아트워크를 주기적으로 교체하고 있으며, 다양한 소품이 준비되어 있습니다.','서울특별시 금천구',10,150000,'2024-12-01 04:14:04.273014','2024-12-01 04:14:04.273014',2,'https://i.ibb.co/BgBg90T/t600-20240517161214-41841.jpg');
/*!40000 ALTER TABLE `space` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `space_category`
--

DROP TABLE IF EXISTS `space_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `space_category` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(30) NOT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `category_name` (`category_name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `space_category`
--

LOCK TABLES `space_category` WRITE;
/*!40000 ALTER TABLE `space_category` DISABLE KEYS */;
INSERT INTO `space_category` VALUES (5,'갤러리'),(6,'공연장'),(7,'공유주방'),(8,'스튜디오'),(3,'촬영 장소'),(4,'파티룸'),(2,'팝업스토어'),(1,'회의실');
/*!40000 ALTER TABLE `space_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `space_category_mapping`
--

DROP TABLE IF EXISTS `space_category_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `space_category_mapping` (
  `mapping_id` int NOT NULL AUTO_INCREMENT,
  `category_id` int NOT NULL,
  `space_id` int NOT NULL,
  PRIMARY KEY (`mapping_id`),
  UNIQUE KEY `unique_space_category` (`space_id`,`category_id`),
  KEY `idx_category_space` (`category_id`,`space_id`),
  CONSTRAINT `space_category_mappi_category_id_c0664df0_fk_space_cat` FOREIGN KEY (`category_id`) REFERENCES `space_category` (`category_id`),
  CONSTRAINT `space_category_mapping_space_id_aa8aff76_fk_space_space_id` FOREIGN KEY (`space_id`) REFERENCES `space` (`space_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `space_category_mapping`
--

LOCK TABLES `space_category_mapping` WRITE;
/*!40000 ALTER TABLE `space_category_mapping` DISABLE KEYS */;
INSERT INTO `space_category_mapping` VALUES (2,3,1),(1,8,1),(4,4,2),(3,8,2),(5,7,3),(6,8,3),(8,1,4),(7,6,4),(12,2,5),(11,3,5),(9,5,5),(10,8,5);
/*!40000 ALTER TABLE `space_category_mapping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `space_review_avg_view`
--

DROP TABLE IF EXISTS `space_review_avg_view`;
/*!50001 DROP VIEW IF EXISTS `space_review_avg_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `space_review_avg_view` AS SELECT 
 1 AS `space_id`,
 1 AS `average_rating`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `space_with_category_view`
--

DROP TABLE IF EXISTS `space_with_category_view`;
/*!50001 DROP VIEW IF EXISTS `space_with_category_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `space_with_category_view` AS SELECT 
 1 AS `space_id`,
 1 AS `space_name`,
 1 AS `description`,
 1 AS `address`,
 1 AS `capacity`,
 1 AS `price_per_date`,
 1 AS `user_id`,
 1 AS `space_created_at`,
 1 AS `space_updated_at`,
 1 AS `categories`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(100) NOT NULL,
  `user_name` varchar(15) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `role` enum('host','guest') NOT NULL,
  `user_created_at` datetime(6) NOT NULL,
  `user_updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  KEY `idx_email_role` (`email`,`role`),
  KEY `idx_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'1','김동국','host1@gmail.com','1234','host','2024-12-01 03:51:19.795288','2024-12-01 03:51:19.795288'),(2,'1','이명진','host2@gmail.com','4123','host','2024-12-01 03:51:47.541074','2024-12-01 03:51:47.541074'),(3,'1','노래하는 하리보','guest1@gmail.com','9876','guest','2024-12-01 03:52:34.832646','2024-12-01 03:52:34.832646'),(4,'1','춤추는 바지','guest2@gmail.com','5432','guest','2024-12-01 03:53:06.053523','2024-12-01 03:53:06.053523'),(5,'1','등산하는 라이언','guest3@gmail.com','7654','guest','2024-12-01 03:53:28.883020','2024-12-01 03:53:28.883020'),(6,'1','잠자는 코끼리','guest4@gmail.com','3456','guest','2024-12-01 03:53:55.966563','2024-12-01 03:53:55.966563');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `user_booking_view`
--

DROP TABLE IF EXISTS `user_booking_view`;
/*!50001 DROP VIEW IF EXISTS `user_booking_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `user_booking_view` AS SELECT 
 1 AS `booking_id`,
 1 AS `user_name`,
 1 AS `email`,
 1 AS `phone`,
 1 AS `space_name`,
 1 AS `image`,
 1 AS `address`,
 1 AS `start_date`,
 1 AS `end_date`,
 1 AS `booking_status`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `space_review_avg_view`
--

/*!50001 DROP VIEW IF EXISTS `space_review_avg_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb3 */;
/*!50001 SET character_set_results     = utf8mb3 */;
/*!50001 SET collation_connection      = utf8mb3_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `space_review_avg_view` AS select `b`.`space_id` AS `space_id`,avg(`r`.`review_rating`) AS `average_rating` from (`review` `r` join `booking` `b` on((`r`.`booking_id` = `b`.`booking_id`))) group by `b`.`space_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `space_with_category_view`
--

/*!50001 DROP VIEW IF EXISTS `space_with_category_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb3 */;
/*!50001 SET character_set_results     = utf8mb3 */;
/*!50001 SET collation_connection      = utf8mb3_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `space_with_category_view` AS select `s`.`space_id` AS `space_id`,`s`.`space_name` AS `space_name`,`s`.`description` AS `description`,`s`.`address` AS `address`,`s`.`capacity` AS `capacity`,`s`.`price_per_date` AS `price_per_date`,`s`.`user_id` AS `user_id`,`s`.`space_created_at` AS `space_created_at`,`s`.`space_updated_at` AS `space_updated_at`,group_concat(`c`.`category_name` order by `c`.`category_name` ASC separator ', ') AS `categories` from ((`space` `s` left join `space_category_mapping` `scm` on((`s`.`space_id` = `scm`.`space_id`))) left join `space_category` `c` on((`scm`.`category_id` = `c`.`category_id`))) group by `s`.`space_id`,`s`.`space_name`,`s`.`description`,`s`.`address`,`s`.`capacity`,`s`.`price_per_date`,`s`.`user_id`,`s`.`space_created_at`,`s`.`space_updated_at` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `user_booking_view`
--

/*!50001 DROP VIEW IF EXISTS `user_booking_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb3 */;
/*!50001 SET character_set_results     = utf8mb3 */;
/*!50001 SET collation_connection      = utf8mb3_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `user_booking_view` AS select `b`.`booking_id` AS `booking_id`,`u`.`user_name` AS `user_name`,`u`.`email` AS `email`,`u`.`phone` AS `phone`,`s`.`space_name` AS `space_name`,`s`.`image` AS `image`,`s`.`address` AS `address`,`b`.`start_date` AS `start_date`,`b`.`end_date` AS `end_date`,`b`.`booking_status` AS `booking_status` from ((`booking` `b` join `space` `s` on((`b`.`space_id` = `s`.`space_id`))) join `user` `u` on((`b`.`user_id` = `u`.`user_id`))) order by `b`.`booking_created_at` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-01 14:52:32
