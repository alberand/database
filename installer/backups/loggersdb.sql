-- MySQL dump 10.16  Distrib 10.1.19-MariaDB, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: 127.0.0.1
-- ------------------------------------------------------
-- Server version	10.1.19-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Position to start replication or point-in-time recovery from
--

-- CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000072', MASTER_LOG_POS=366;

--
-- GTID to start replication from
--

-- SET GLOBAL gtid_slave_pos='0-1-2178';

--
-- Current Database: `loggersdb`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `loggersdb` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `loggersdb`;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add loggers',7,'add_loggers'),(20,'Can change loggers',7,'change_loggers'),(21,'Can delete loggers',7,'delete_loggers'),(22,'Can add messages',8,'add_messages'),(23,'Can change messages',8,'change_messages'),(24,'Can delete messages',8,'delete_messages'),(25,'Can add packages',9,'add_packages'),(26,'Can change packages',9,'change_packages'),(27,'Can delete packages',9,'delete_packages');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(7,'loggers_ui','loggers'),(8,'loggers_ui','messages'),(9,'loggers_ui','packages'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'loggers_ui','0001_initial','2016-08-10 14:45:10.883480'),(2,'contenttypes','0001_initial','2016-08-10 19:19:03.278006'),(3,'auth','0001_initial','2016-08-10 19:19:04.918002'),(4,'admin','0001_initial','2016-08-10 19:19:05.273894'),(5,'admin','0002_logentry_remove_auto_add','2016-08-10 19:19:05.305813'),(6,'contenttypes','0002_remove_content_type_name','2016-08-10 19:19:05.587350'),(7,'auth','0002_alter_permission_name_max_length','2016-08-10 19:19:05.741921'),(8,'auth','0003_alter_user_email_max_length','2016-08-10 19:19:05.860151'),(9,'auth','0004_alter_user_username_opts','2016-08-10 19:19:05.876159'),(10,'auth','0005_alter_user_last_login_null','2016-08-10 19:19:05.996610'),(11,'auth','0006_require_contenttypes_0002','2016-08-10 19:19:06.009938'),(12,'auth','0007_alter_validators_add_error_messages','2016-08-10 19:19:06.026206'),(13,'auth','0008_alter_user_username_max_length','2016-08-10 19:19:06.151954'),(14,'sessions','0001_initial','2016-08-10 19:19:06.255489');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ses_id` int(11) NOT NULL,
  `ses_time` time DEFAULT NULL,
  `msg` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `msg_session` (`ses_id`),
  CONSTRAINT `msg_session` FOREIGN KEY (`ses_id`) REFERENCES `sessions` (`ses_id`)
) ENGINE=InnoDB AUTO_INCREMENT=138 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (117,93810,'00:00:00','Reset'),(118,93810,'00:00:05','Init wait done.'),(119,93810,'00:00:05','Modem init done.'),(120,93810,'00:00:00','Reset'),(121,93810,'00:00:05','Init wait done.'),(122,93810,'00:00:05','Modem init done.'),(123,15053,'00:00:00','Reset'),(124,15053,'00:00:05','Init wait done.'),(125,15053,'00:00:05','Modem init done.'),(126,15053,'00:00:00','Reset'),(127,15053,'00:00:05','Init wait done.'),(128,15053,'00:00:05','Modem init done.'),(135,63547,'00:00:00','Reset'),(136,63547,'00:00:05','Init wait done.'),(137,63547,'00:00:05','Modem init done.');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `packages`
--

DROP TABLE IF EXISTS `packages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `packages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ses_id` int(11) NOT NULL,
  `module_id` int(11) DEFAULT NULL,
  `ses_time` time DEFAULT NULL,
  `date` date DEFAULT NULL,
  `time` time DEFAULT NULL,
  `t_ms` int(11) DEFAULT NULL,
  `latitude` float(10,5) DEFAULT NULL,
  `lat_pos` enum('N','S') DEFAULT NULL,
  `longitude` float(10,5) DEFAULT NULL,
  `lon_pos` enum('E','W') DEFAULT NULL,
  `course` float DEFAULT NULL,
  `gps_altitude` float(4,1) DEFAULT NULL,
  `speed` float DEFAULT NULL,
  `temperature` int(11) DEFAULT NULL,
  `pressure` int(11) DEFAULT NULL,
  `gps_state` int(11) DEFAULT NULL,
  `sat_num` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pkg_session` (`ses_id`),
  CONSTRAINT `pkg_session` FOREIGN KEY (`ses_id`) REFERENCES `sessions` (`ses_id`)
) ENGINE=InnoDB AUTO_INCREMENT=538 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `packages`
--

LOCK TABLES `packages` WRITE;
/*!40000 ALTER TABLE `packages` DISABLE KEYS */;
INSERT INTO `packages` VALUES (374,93810,NULL,NULL,'2016-09-03','18:20:30',900000,1423.54456,'N',5004.88135,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(375,93810,NULL,NULL,'2016-09-03','18:20:31',900000,1423.54529,'N',5004.88916,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(376,93810,NULL,NULL,'2016-09-03','18:20:32',900000,1423.56470,'N',5004.88867,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(377,93810,NULL,NULL,'2016-09-03','18:20:33',900000,1423.58032,'N',5004.85400,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(378,93810,NULL,NULL,'2016-09-03','18:20:34',900000,1423.58276,'N',5004.84521,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(379,93810,NULL,NULL,'2016-09-03','18:20:35',900000,1423.68018,'N',5004.82080,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(380,93810,NULL,NULL,'2016-09-03','18:20:36',900000,1423.73706,'N',5004.81445,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(381,93810,NULL,NULL,'2016-09-03','18:20:37',900000,1423.78406,'N',5004.78467,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(382,93810,NULL,NULL,'2016-09-03','18:20:38',900000,1423.78979,'N',5004.77832,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(383,93810,NULL,NULL,'2016-09-03','18:20:39',900000,1423.79956,'N',5004.78174,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(384,93810,NULL,NULL,'2016-09-03','18:20:40',900000,1423.80725,'N',5004.77344,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(385,93810,NULL,NULL,'2016-09-03','18:20:41',900000,1423.80981,'N',5004.76953,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(386,93810,NULL,NULL,'2016-09-03','18:20:42',900000,1423.81775,'N',5004.76562,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(387,93810,NULL,NULL,'2016-09-03','18:20:43',900000,1423.80200,'N',5004.75098,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(388,93810,NULL,NULL,'2016-09-03','18:20:44',900000,1423.80347,'N',5004.74951,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(389,93810,NULL,NULL,'2016-09-03','18:20:45',900000,1423.81946,'N',5004.75098,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(390,93810,NULL,NULL,'2016-09-03','18:20:46',900000,1423.83179,'N',5004.75439,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(391,93810,NULL,NULL,'2016-09-03','18:20:47',900000,1423.83826,'N',5004.75488,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(392,93810,NULL,NULL,'2016-09-03','18:20:48',900000,1423.84082,'N',5004.75146,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(393,93810,NULL,NULL,'2016-09-03','18:20:49',900000,1423.82922,'N',5004.74316,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(394,93810,NULL,NULL,'2016-09-03','18:20:50',900000,1423.82764,'N',5004.74023,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(395,93810,NULL,NULL,'2016-09-03','18:20:51',900000,1423.81042,'N',5004.73975,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(396,93810,NULL,NULL,'2016-09-03','18:20:52',900000,1423.80115,'N',5004.73730,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(397,93810,NULL,NULL,'2016-09-03','18:20:53',900000,1423.80005,'N',5004.73438,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(398,93810,NULL,NULL,'2016-09-03','18:20:54',900000,1423.80359,'N',5004.72852,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(399,93810,NULL,NULL,'2016-09-03','18:20:55',900000,1423.80811,'N',5004.72900,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(400,93810,NULL,NULL,'2016-09-03','18:20:56',900000,1423.81018,'N',5004.72119,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(401,93810,NULL,NULL,'2016-09-03','18:20:57',900000,1423.83374,'N',5004.71484,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(402,93810,NULL,NULL,'2016-09-03','18:20:58',900000,1423.83655,'N',5004.71143,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(403,93810,NULL,NULL,'2016-09-03','18:20:59',900000,1423.83716,'N',5004.70801,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(404,93810,NULL,NULL,'2016-09-03','18:21:00',900000,1423.84705,'N',5004.70459,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(405,93810,NULL,NULL,'2016-09-03','18:21:01',900000,1423.86060,'N',5004.70361,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(406,93810,NULL,NULL,'2016-09-03','18:21:02',900000,1423.88306,'N',5004.70410,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(407,93810,NULL,NULL,'2016-09-03','18:21:03',900000,1423.89075,'N',5004.70361,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(408,93810,NULL,NULL,'2016-09-03','18:21:04',900000,1423.87634,'N',5004.69434,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(409,93810,NULL,NULL,'2016-09-03','18:21:05',900000,1423.86951,'N',5004.69092,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(410,93810,NULL,NULL,'2016-09-03','18:21:06',900000,1423.86829,'N',5004.68848,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(411,93810,NULL,NULL,'2016-09-03','18:21:07',900000,1423.86926,'N',5004.68652,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(412,93810,NULL,NULL,'2016-09-03','18:21:08',900000,1423.87354,'N',5004.68555,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(413,93810,NULL,NULL,'2016-09-03','18:21:09',900000,1423.88269,'N',5004.68750,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(414,93810,NULL,NULL,'2016-09-03','18:21:10',900000,1423.88965,'N',5004.68750,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(415,93810,NULL,NULL,'2016-09-03','18:21:11',900000,1423.89795,'N',5004.68311,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(416,93810,NULL,NULL,'2016-09-03','18:21:12',900000,1423.90869,'N',5004.68213,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(417,93810,NULL,NULL,'2016-09-03','18:21:13',900000,1423.91394,'N',5004.67871,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(418,93810,NULL,NULL,'2016-09-03','18:21:14',900000,1423.89990,'N',5004.67773,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(419,93810,NULL,NULL,'2016-09-03','18:21:15',900000,1423.88623,'N',5004.67480,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(420,93810,NULL,NULL,'2016-09-03','18:21:16',900000,1423.87854,'N',5004.67334,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(421,93810,NULL,NULL,'2016-09-03','18:21:17',900000,1423.87268,'N',5004.67041,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(422,93810,NULL,NULL,'2016-09-03','18:21:18',900000,1423.87122,'N',5004.66455,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(423,93810,NULL,NULL,'2016-09-03','18:21:19',900000,1423.87427,'N',5004.65967,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(424,93810,NULL,NULL,'2016-09-03','18:21:20',900000,1423.87903,'N',5004.65820,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(461,93810,NULL,NULL,'2016-09-03','18:21:57',900000,1424.21875,'N',5004.47266,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(462,93810,NULL,NULL,'2016-09-03','18:21:58',900000,1424.21643,'N',5004.47119,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(463,93810,NULL,NULL,'2016-09-03','18:21:59',900000,1424.21692,'N',5004.46631,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(464,93810,NULL,NULL,'2016-09-03','18:22:00',900000,1424.21948,'N',5004.46533,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(465,93810,NULL,NULL,'2016-09-04','18:22:01',900000,1424.22168,'N',5004.41699,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(490,15053,NULL,NULL,'2016-09-03','18:20:30',900000,1423.54932,'N',5004.88916,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(491,15053,NULL,NULL,'2016-09-03','18:20:31',900000,1423.54932,'N',5004.88916,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(492,15053,NULL,NULL,'2016-09-03','18:20:32',900000,1423.56970,'N',5004.88867,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(493,15053,NULL,NULL,'2016-09-03','18:20:33',900000,1423.58936,'N',5004.85400,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(494,15053,NULL,NULL,'2016-09-03','18:20:34',900000,1423.58984,'N',5004.84521,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(495,15053,NULL,NULL,'2016-09-03','18:20:35',900000,1423.68921,'N',5004.82080,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(496,15053,NULL,NULL,'2016-09-03','18:20:36',900000,1423.73901,'N',5004.81445,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(497,15053,NULL,NULL,'2016-09-03','18:20:37',900000,1423.78894,'N',5004.78467,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(498,15053,NULL,NULL,'2016-09-03','18:20:38',900000,1423.78979,'N',5004.77832,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(499,15053,NULL,NULL,'2016-09-03','18:20:39',900000,1423.79956,'N',5004.78174,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(500,15053,NULL,NULL,'2016-09-03','18:20:40',900000,1423.80920,'N',5004.77344,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(501,15053,NULL,NULL,'2016-09-03','18:20:41',900000,1423.80981,'N',5004.76953,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(526,63547,NULL,NULL,'2016-09-03','18:20:30',900000,3.54929,'N',5004.88916,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(527,63547,NULL,NULL,'2016-09-03','18:20:31',900000,3.54930,'N',5004.88916,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(528,63547,NULL,NULL,'2016-09-03','18:20:32',900000,3.56970,'N',5004.88867,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(529,63547,NULL,NULL,'2016-09-03','18:20:33',900000,3.58930,'N',5004.85400,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(530,63547,NULL,NULL,'2016-09-03','18:20:34',900000,3.58980,'N',5004.84521,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(531,63547,NULL,NULL,'2016-09-03','18:20:35',900000,3.68920,'N',5004.82080,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(532,63547,NULL,NULL,'2016-09-03','18:20:36',900000,3.73900,'N',5004.81445,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(533,63547,NULL,NULL,'2016-09-03','18:20:37',900000,3.78900,'N',5004.78467,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(534,63547,NULL,NULL,'2016-09-03','18:20:38',900000,3.78980,'N',5004.77832,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(535,63547,NULL,NULL,'2016-09-03','18:20:39',900000,3.79950,'N',5004.78174,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(536,63547,NULL,NULL,'2016-09-03','18:20:40',900000,3.80920,'N',5004.77344,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(537,63547,NULL,NULL,'2016-09-03','18:20:41',900000,3.80980,'N',5004.76953,'E',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `packages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sessions` (
  `ses_id` int(11) NOT NULL,
  PRIMARY KEY (`ses_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
INSERT INTO `sessions` VALUES (15053),(63547),(93810);
/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-11-18 12:01:20
