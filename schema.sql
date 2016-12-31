-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versione server:              10.0.28-MariaDB-0ubuntu0.16.04.1 - Ubuntu 16.04
-- S.O. server:                  debian-linux-gnu
-- HeidiSQL Versione:            9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dump della struttura del database levbod
CREATE DATABASE IF NOT EXISTS `levbod` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `levbod`;

-- Dump della struttura di tabella levbod.beatmapsets
DROP TABLE IF EXISTS `beatmapsets`;
CREATE TABLE IF NOT EXISTS `beatmapsets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `beatmapset_id` int(11) NOT NULL DEFAULT '0',
  `ranked_status` tinyint(4) NOT NULL DEFAULT '0',
  `last_update` int(11) NOT NULL DEFAULT '0',
  `artist` varchar(50) NOT NULL DEFAULT '0',
  `title` varchar(50) NOT NULL DEFAULT '0',
  `creator` varchar(50) NOT NULL DEFAULT '0',
  `source` varchar(50) NOT NULL DEFAULT '0',
  `tags` varchar(50) NOT NULL DEFAULT '0',
  `has_video` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `beatmapset_id` (`beatmapset_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- L’esportazione dei dati non era selezionata.
-- Dump della struttura di tabella levbod.child_beatmaps
DROP TABLE IF EXISTS `child_beatmaps`;
CREATE TABLE IF NOT EXISTS `child_beatmaps` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `beatmap_id` int(11) NOT NULL DEFAULT '0',
  `beatmapset_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `beatmapset_id` (`beatmapset_id`),
  KEY `beatmap_id` (`beatmap_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- L’esportazione dei dati non era selezionata.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
