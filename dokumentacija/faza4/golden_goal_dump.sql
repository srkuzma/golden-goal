CREATE DATABASE  IF NOT EXISTS `golden_goal` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `golden_goal`;
-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: localhost    Database: golden_goal
-- ------------------------------------------------------
-- Server version	8.0.27

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'administrator'),(2,'moderator'),(3,'user');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (5,1,22),(6,1,23),(7,1,24),(1,1,39),(2,1,40),(3,1,43),(4,1,44),(8,2,37),(9,2,38),(10,2,39),(11,2,40),(12,2,44),(19,3,28),(13,3,32),(14,3,33),(15,3,36),(16,3,40),(17,3,41),(18,3,44);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `text` longtext NOT NULL,
  `date_time` datetime(6) NOT NULL,
  `author_id` bigint NOT NULL,
  `comment_reply_id` bigint DEFAULT NULL,
  `news_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `comment_author_id_36cf9cf3_fk_user_id` (`author_id`),
  KEY `comment_comment_reply_id_8c31d3f5_fk_comment_id` (`comment_reply_id`),
  KEY `comment_news_id_36f14eae_fk_news_id` (`news_id`),
  CONSTRAINT `comment_author_id_36cf9cf3_fk_user_id` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`),
  CONSTRAINT `comment_comment_reply_id_8c31d3f5_fk_comment_id` FOREIGN KEY (`comment_reply_id`) REFERENCES `comment` (`id`),
  CONSTRAINT `comment_news_id_36f14eae_fk_news_id` FOREIGN KEY (`news_id`) REFERENCES `news` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (1,'Amazing preview!','2022-06-01 22:26:33.115716',3,NULL,5),(2,'This is going to be an interesting game.','2022-06-01 22:27:35.938868',4,NULL,5),(3,'It will not be, both teams are not in great form.','2022-06-01 22:28:17.000000',6,2,5),(4,'Great addition for Arsenal!','2022-06-02 21:45:31.855035',3,NULL,1),(5,'Great addition for Arsenal!','2022-06-02 21:54:30.500125',11,NULL,1);
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `news`
--

DROP TABLE IF EXISTS `news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `news` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `summary` longtext NOT NULL,
  `content` longtext NOT NULL,
  `date_time` datetime(6) NOT NULL,
  `author_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `news_author_id_064efc6e_fk_user_id` (`author_id`),
  CONSTRAINT `news_author_id_064efc6e_fk_user_id` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news`
--

LOCK TABLES `news` WRITE;
/*!40000 ALTER TABLE `news` DISABLE KEYS */;
INSERT INTO `news` VALUES (1,'Arsenal set to sign Sao Paulo striker Marquinhos','Arsenal are closing in on a €3.5 million deal with Sao Paulo for teenage striker Marquinhos, sources have told ESPN. The two clubs agreed a fee after the 19-year-old rejected multiple contract offers from the Brazilian club and sources suggest Arsenal moved quickly to secure a cut-price agreement.','Arsenal are closing in on a €3.5 million deal with Sao Paulo for teenage striker Marquinhos, sources have told ESPN.\r\n\r\nThe two clubs agreed a fee after the 19-year-old rejected multiple contract offers from the Brazilian club and sources suggest Arsenal moved quickly to secure a cut-price agreement.\r\n\r\nMarquinhos is a left-footed forward also able to operate as a winger but he is viewed by Arsenal as a future prospect rather than an immediate first-team signing.\r\n\r\nPersonal terms are yet to be finalised but an agreement is expected soon. Arsenal remain in the market for at least one striker this summer with Eddie Nketiah and Alexandre Lacazette both out of contract at the end of the season.\r\n\r\nArsenal have explored the possibility of signing Manchester City\'s Gabriel Jesus and have also contacted Paulo Dybala\'s representatives with the Argentine set to leave Juventus on a free transfer at the end of the season.','2022-06-01 19:33:26.373281',2),(2,'Man United to miss out on £12m Andreas Pereira fee','Manchester United are set to miss out on a £12 million transfer fee for Andreas Pereira, sources have told ESPN, with Brazilian club Flamengo preparing to abandon a deal to sign the midfielder at the end of his season-long loan spell. Pereira, 26, moved to Flamengo last August with United giving the two-time Copa Libertadores winners an option to sign the Belgium-born Brazil international for a fee rising to £12m based on appearances.','Manchester United are set to miss out on a £12 million transfer fee for Andreas Pereira, sources have told ESPN, with Brazilian club Flamengo preparing to abandon a deal to sign the midfielder at the end of his season-long loan spell.\r\n\r\nPereira, 26, moved to Flamengo last August with United giving the two-time Copa Libertadores winners an option to sign the Belgium-born Brazil international for a fee rising to £12m based on appearances.\r\n\r\nBut despite making 34 appearances in all competitions for the Rio de Janeiro-based team, sources have told ESPN that Pereira has not done enough to convince Flamengo to complete a permanent move for the midfielder.\r\n\r\nHaving signed for United as a 15-year-old in 2011 after leaving the youth ranks of PSV Eindhoven, Pereira has struggled to realise his potential in the first-team at Old Trafford.\r\n\r\nLoan moves to Spanish clubs Granada and Valencia, followed by another temporary move to Serie A with Lazio, have restricted Pereira to just 75 senior appearances for United.\r\n\r\nSources have said that Pereira moved to Flamengo in the hope of re-launching his career and was prepared to take a substantial pay-cut to seal a permanent move to the club.\r\n\r\nBut a costly mistake in the Copa Libertadores final defeat against Palmeiras last November, when a bad pass in extra-time gifted Flamengo\'s opponents a goal to claim a 2-1 win, has impacted on Pereira\'s performances and a return to Old Trafford is now the most likely outcome for the player, who still has a year to run on his United contract.\r\n\r\nSources have told ESPN that United are still hopeful that a deal can be done with Flamengo, who may yet be prepared to sign Pereira for a reduced fee.','2022-06-01 19:33:26.373281',2),(3,'Brazilian derby called off as Internacional fans smash Gremio team bus','One of Brazil\'s biggest derby matches was canceled shortly before kick-off on Saturday, after players from Gremio were hurt when fans attacked their team bus on the way to a game against city rivals Internacional. The match between the two main clubs in Porto Alegre is known as the Grenal but Gremio withdrew from the match at Inter\'s Beira-Rio stadium after rocks smashed through coach windows and hurt players. Gremio posted a picture of midfielder Mathias Villasanti being taken to hospital in an ambulance. It also showed photographs of smashed windows and a rock bigger than a fist it said hit the Paraguayan player.','One of Brazil\'s biggest derby matches was canceled shortly before kick-off on Saturday, after players from Gremio were hurt when fans attacked their team bus on the way to a game against city rivals Internacional.\r\n\r\nThe match between the two main clubs in Porto Alegre is known as the Grenal but Gremio withdrew from the match at Inter\'s Beira-Rio stadium after rocks smashed through coach windows and hurt players.\r\n\r\nGremio posted a picture of midfielder Mathias Villasanti being taken to hospital in an ambulance. It also showed photographs of smashed windows and a rock bigger than a fist it said hit the Paraguayan player.\r\n\r\n\"After the cowardly and absurd aggression suffered by our delegation we have told the Gaucha Football Federation of our decision not to go ahead with the Grenal derby this Saturday,\" Gremio said.\r\n\r\n\"In addition to the technical imbalance and the absence of sporting atmosphere this criminal act causes, Gremio\'s decision also shows our repudiation of all kinds of violence.\"\r\n\r\nInternacional also said it repudiated the violence, adding that two suspects had been arrested.\r\n\r\nGremio later said Villasanti, 25, was being treated for cerebral concussion and cranial trauma. He was also being treated for lacerations to the face and trauma in his hip and would spent the night in hospital for further observation.\r\n\r\nNo fractures were reported.\r\n\r\nIt was the second time in three days that a bus carrying a Brazilian team had been attacked on its way to a game, after Bahia players were hit before Thursday night\'s match against Sampaio Correa in Salvador.\r\n\r\nThe Porto Alegre incident also took place the same night that fans wielding metal bars invaded the pitch and attacked Parana players, forcing the suspension of their game against Uniao Beltrao in Curitiba.\r\n\r\nWith around five minutes to go in the state championship match, Parana were losing 3-1, a result that doomed them to relegation to the second division.\r\n\r\nVideos showed angry fans punching players, who responded with kung fu kicks as other supporters poured on to the field to join the fighting.\r\n\r\nBoth sets of players eventually managed to sprint to the dressing rooms as police fired percussion grenades and forced fans off the pitch.','2022-06-01 19:33:26.373281',2),(4,'Internacional join race to sign NYCFC\'s Taty Castellanos','Brazilian Serie A side Internacional is the latest South American club to enter the race for New York City FC forward Taty Castellanos, sources have confirmed to ESPN. Inter\'s interest was first reported by Brazil-based outlet GE. Inter has money to spend after concluding the transfer of Yuri Alberto to Zenit St. Petersburg for $22 million, though one source cautioned that negotiations are in the early stages. Inter recently acquired Aston Villa attacker Wesley Moraes after he cut short his loan with Club Brugge.','Brazilian Serie A side Internacional is the latest South American club to enter the race for New York City FC forward Taty Castellanos, sources have confirmed to ESPN.\r\n\r\nInter\'s interest was first reported by Brazil-based outlet GE.\r\n\r\nInter has money to spend after concluding the transfer of Yuri Alberto to Zenit St. Petersburg for $22 million, though one source cautioned that negotiations are in the early stages. Inter recently acquired Aston Villa attacker Wesley Moraes after he cut short his loan with Club Brugge.\r\n\r\nRiver Plate has also shown interest, and Castellanos has spoken of his dream to one day play for the Argentine giants.\r\n\r\nRiver\'s plan is to sign Castellanos for the start of the 2022 Copa Libertadores, which begins in April.\r\n\r\nReports have said that Italy Serie A side Fiorentina are looking at Castellanos as well, but they recently signed forwards Arthur Cabral from Basel and Krzysztof Piatek from Hertha Berlin.\r\n\r\nSources have told ESPN that would like to receive between $15m to $20m on a deal.\r\n\r\nBrazilian Serie A side Palmeiras made an offer of about $12.5m, which the MLS team rejected, though sources have told ESPN that the Verdao remain interested in the striker.\r\n\r\nBrazil\'s transfer window closes on April 12, while Argentina\'s will conclude on Feb.19.\r\n\r\nA native of Mendoza, Argentina, Castellanos originally joined NYCFC on loan in 2018 from Uruguayan side Montevideo City Torque, another City Football Group club. He made the move permanent at the conclusion of that season.\r\n\r\nIn 35 league and playoff appearances in 2021, Castellanos scored 22 goals and added eight assists while winning the Golden Boot. He also scored in the MLS Cup final triumph over the Portland Timbers. In parts of four seasons with NYCFC, he scored 40 goals with 18 assists in 99 league and playoff appearances.','2022-06-01 19:33:26.373281',2),(5,'Preview: Atletico Goianiense vs. Corinthians','Atletico Goianiense have a chance to move out of the relegation zone with a victory on Saturday at Atletico Clube Goianiense Stadium versus Corinthians. Dragao are unbeaten in their previous four matches played in all competitions, while Timao are currently in a three-way tie for the top spot in the Campeonato Brasileiro Serie A after being held to a draw last weekend for a third successive league fixture.','Atletico Goianiense have a chance to move out of the relegation zone with a victory on Saturday at Atletico Clube Goianiense Stadium versus Corinthians.\r\n\r\nDragao are unbeaten in their previous four matches played in all competitions, while Timao are currently in a three-way tie for the top spot in the Campeonato Brasileiro Serie A after being held to a draw last weekend for a third successive league fixture.\r\n\r\nSlowly but surely, the club from Goiania are climbing their way out of relegation danger, collecting a point in four of their last six league games.\r\n\r\nSince the arrival of Jorginho as manager, these players have shown a relentless resolve, which has eventually paid off, scoring with 11 minutes remaining to earn a draw against Internacional on Monday (1-1) after firing home a late goal in each half the previous week to defeat Coritiba (2-0).\r\n\r\nFor the time being Goianiense are doing just enough to get by, scoring a goal or fewer in all but one of their eight league fixtures this season.\r\n\r\nThey have not shown a lot of attacking qualities this year, but that has not mattered in recent home games, where Dragao have managed to collect two successive clean sheets in all competitions.\r\n\r\nGoianiense have never beaten Corinthians on their current home field though, with their last home triumph against them coming at Estadio Serra Dourada.\r\n\r\nAtletico still sustain their share of pressure in their third of the field, but they seem to be doing a better job at managing that intensity as their defenders have been in the correct positions to block plenty of clear-cut scoring opportunities.\r\n\r\nThe season is still young, however, an eighth Brasileiro Serie A title is still very much in the cards for Vitor Pereira and Corinthians.\r\n\r\nPereira has a winning track record during his time with FC Porto, winning a pair of domestic championships in Portugal, and he will hope to replicate the recent success of other Portuguese managers like Abel Ferreira, who has led Palmeiras to back-to-back Copa Libertadores titles.\r\n\r\nCorinthians are off to their best start to a domestic campaign since 2017, when they went unbeaten in their opening 19 matches en route to being crowned Brasileiro Serie A champions later that year.\r\n\r\nWhile there is a lot to like about how aggressive and forward-thinking they are in their approach, Timao have had to dig themselves out of several holes lately, trailing four times in their previous three league encounters, but still managing to earn a single point every time.\r\n\r\nEven though their only defeat came away from home, they have usually maintained their focus in enemy territory, with half of their victories coming on the road.\r\n\r\nPereira has called on his players to be more aggressive when it comes to closing down attacking players, using a more man-oriented system which has made it difficult for opposing teams to penetrate their backline.','2022-06-01 22:24:04.450277',2),(6,'Preview: America Mineiro vs. Cuiaba','America Mineiro and Cuiaba will be out to end their winless runs across all competitions when they go head to head at the Arena Independencia in Brasileiro action on Saturday. The hosts picked up an impressive draw at then league-leaders Corinthians last weekend, whilst the visitors suffered yet another defeat as they dropped into the relegation zone.','America Mineiro and Cuiaba will be out to end their winless runs across all competitions when they go head to head at the Arena Independencia in Brasileiro action on Saturday.\r\n\r\nThe hosts picked up an impressive draw at then league-leaders Corinthians last weekend, whilst the visitors suffered yet another defeat as they dropped into the relegation zone.\r\n\r\nDespite the excellent point earned at leaders Corinthians last time out, Mineiro boss Vagner Mancini will have been disappointed that his side did not return home with all three.\r\n\r\nA fantastic defensive display saw his side limit their hosts to very little action in front of goal, whilst also possessing a constant danger on the counter attack at the other end of the pitch.\r\n\r\nOnce Aloisio had given Mineiro the lead midway through the second half, Mancini will have been expecting his side to see out the rest of the game and record a memorable victory, particularly after entering the final 10 minutes with the one-goal advantage still intact.\r\n\r\nHowever, Gustavo Silva equalised for Corinthians eight minutes from normal time to send Mineiro home with a share of the points instead.\r\n\r\nDespite putting in an admirable display and picking up a positive result, Mineiro now find themselves on a five-game winless streak across all competitions, with a disappointing cup exit in the Copa Libertadores coming a few days prior to the trip to Corinthians.\r\n\r\nHowever, Saturday\'s hosts still find themselves in a comfortable position of 10th in the Brasileiro heading into matchday nine, remaining consistent with their eighth-placed finish upon their return to the top flight in the 2021 campaign.\r\n\r\nMeanwhile, Cuiaba head to the Arena Independencia on Saturday still under the stewardship of youth team coach William Araujo following the departure of Pintado back in May.\r\n\r\nAraujo oversaw an excellent victory at River Plate in the Copa Sudamericana in his first game in temporary charge, but has since gone on to draw with Internacional, and lose successive games against Melgar and Athletico Paranaense.\r\n\r\nAs a result, it is just one win in 10 games across all competitions for Cuiaba ahead of Saturday\'s Brasileiro encounter with Mineiro, whom they have beaten just once in six previous meetings in the top flight and Serie B.\r\n\r\nLast weekend\'s 1-0 defeat to Paranaense sees Cuiaba begin the weekend inside the relegation places, but with only eight games into the 2022 campaign, there remains plenty of time for Araujo and his side to turn their fortunes around.\r\n\r\nHaving picked up six of their eight points so far on their travels this season, Cuiaba will perhaps possess greater confidence being away from the Arena Pantanal on Saturday, so should they manage to turn their home form around, continued success on the road could see them climb back up the table at an impressive rate over the coming weeks.','2022-06-02 21:58:14.000833',5);
/*!40000 ALTER TABLE `news` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prediction`
--

DROP TABLE IF EXISTS `prediction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prediction` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `game` int NOT NULL,
  `type` varchar(2) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `prediction_primary_key` (`user_id`,`game`),
  CONSTRAINT `prediction_user_id_7ec0c8c8_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prediction`
--

LOCK TABLES `prediction` WRITE;
/*!40000 ALTER TABLE `prediction` DISABLE KEYS */;
INSERT INTO `prediction` VALUES (1,390320,'X',3),(2,390312,'2',3),(3,390313,'21',3),(4,390315,'1',3);
/*!40000 ALTER TABLE `prediction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `present`
--

DROP TABLE IF EXISTS `present`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `present` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type` varchar(45) NOT NULL,
  `image` int DEFAULT NULL,
  `points` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `present_user_id_7f33e84d_fk_user_id` (`user_id`),
  CONSTRAINT `present_user_id_7f33e84d_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `present`
--

LOCK TABLES `present` WRITE;
/*!40000 ALTER TABLE `present` DISABLE KEYS */;
INSERT INTO `present` VALUES (1,'double_prediction',NULL,NULL,6),(2,'image',25,NULL,6),(3,'image',29,NULL,6);
/*!40000 ALTER TABLE `present` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `type` varchar(20) NOT NULL,
  `score` int NOT NULL,
  `double_prediction_counter` int NOT NULL,
  `presents` int NOT NULL,
  `image` varchar(250) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'pbkdf2_sha256$320000$rnGcHRAl03L3Q1FMa1F8Ci$Osj1ZgZThg3Xs0tGEKFW0Q3C6PTofRVKTvfISN96LfY=','2022-06-02 21:45:19.301660',1,'kovacd','','','',1,1,'2022-06-01 17:35:42.000000','administrator',0,0,0,'images/image_44.png'),(2,'pbkdf2_sha256$320000$HWWiF6fkAQu20JRGb6BIEO$v4gYlU7lBwQha7C2d9NmuFUJTyh0FoHdMsPyKMsBkFQ=','2022-06-02 18:26:00.159735',0,'dave','','','',0,1,'2022-06-01 17:39:59.000000','moderator',0,0,0,'images/image_44.png'),(3,'pbkdf2_sha256$320000$jzJmDdYcoH1BCBiI12HeBu$RRBzlyu1vj2pb1Rwp+2OaY4VB5d29qutK4+Z8v6uDOc=','2022-06-02 19:44:54.000000',0,'neymar','','','',0,1,'2022-06-01 18:02:16.000000','user',1400,0,0,'images/image_26.png'),(4,'pbkdf2_sha256$320000$s3Sg2BW7ZirpwbordQ8peo$s5oiljOHfVqJVGWBNPk8kExNL8pxsFhWDueISWYWhdk=','2022-06-02 17:27:23.000000',0,'costa','','','',0,1,'2022-06-01 18:02:53.000000','user',3050,1,0,'images/image_36.png'),(5,'pbkdf2_sha256$320000$mFQBY8WeFlc5zOuKI7PB4b$yr7xe1vWUmOsHIWWw0wGY/uz/JA7yh1fohGGgcGfRJg=','2022-06-02 19:56:56.000000',0,'pablo','','','',0,1,'2022-06-01 18:04:26.000000','moderator',0,0,0,'images/image_43.png'),(6,'pbkdf2_sha256$320000$b2CtC6SLKvmkqgh8WczywB$1VdCvtHKLD6N6sPVBkQcDjN7CH4f+YhwdT4UgCuyHis=','2022-06-02 21:45:03.808522',0,'diego','','','',0,1,'2022-06-01 18:05:19.000000','user',2600,3,3,'images/image_40.png'),(7,'pbkdf2_sha256$320000$vfj9y4wMBUAIkKgJtp9sgk$J4iUx9Fk1VAlXODg7uhuOxEXGFDHQ0YkTn0Lnnm3Sqw=','2022-06-02 15:11:57.000000',0,'carlo','','','',0,1,'2022-06-01 18:05:51.000000','user',1600,0,0,'images/image_21.png'),(9,'pbkdf2_sha256$320000$X6ftnAyIC5SVzaBUNVnZnL$R4GTg/RFCi1zgvJTFAHYWjfbBUyh1O6oSEG7cC+BqJ4=','2022-06-02 15:17:31.000000',0,'claudia','','','',0,1,'2022-06-01 18:07:02.000000','user',1400,2,0,'images/image_34.png'),(11,'pbkdf2_sha256$320000$MfgYseqoVL6L1ZlVL1A1T7$zIUqwirwN2reU5AHf6ipbVX3dV92YzQ7eflVnMSSE7w=','2022-06-02 21:39:16.990117',0,'rebeca','','','',0,1,'2022-06-02 19:54:09.000000','user',0,0,0,'images/image_0.png');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_groups`
--

DROP TABLE IF EXISTS `user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_groups_user_id_group_id_40beef00_uniq` (`user_id`,`group_id`),
  KEY `user_groups_group_id_b76f8aba_fk_auth_group_id` (`group_id`),
  CONSTRAINT `user_groups_group_id_b76f8aba_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_groups_user_id_abaea130_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_groups`
--

LOCK TABLES `user_groups` WRITE;
/*!40000 ALTER TABLE `user_groups` DISABLE KEYS */;
INSERT INTO `user_groups` VALUES (1,1,1),(11,2,2),(3,3,3),(4,4,3),(13,5,2),(15,6,3),(7,7,3),(9,9,3),(16,11,3);
/*!40000 ALTER TABLE `user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_image`
--

DROP TABLE IF EXISTS `user_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_image` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` int NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_image_primary_key` (`user_id`,`image`),
  CONSTRAINT `user_image_user_id_91952c7a_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_image`
--

LOCK TABLES `user_image` WRITE;
/*!40000 ALTER TABLE `user_image` DISABLE KEYS */;
INSERT INTO `user_image` VALUES (32,0,1),(33,42,1),(34,43,1),(35,44,1),(36,45,1),(37,46,1),(38,47,1),(39,48,1),(40,49,1),(41,50,1),(11,41,2),(12,42,2),(13,43,2),(14,44,2),(15,45,2),(16,46,2),(4,24,3),(3,25,3),(2,26,3),(1,34,3),(5,28,4),(6,36,4),(17,41,5),(18,42,5),(19,43,5),(20,44,5),(21,45,5),(22,46,5),(9,40,6),(7,21,7),(8,25,7),(10,34,9),(30,0,11);
/*!40000 ALTER TABLE `user_image` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-02 23:46:27
