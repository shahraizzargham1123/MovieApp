-- Cinestream Database Schema (MySQL)

CREATE DATABASE IF NOT EXISTS movie_app
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE movie_app;

-- Users
CREATE TABLE IF NOT EXISTS `user` (
  `id`         INT          NOT NULL AUTO_INCREMENT,
  `username`   VARCHAR(80)  NOT NULL,
  `email`      VARCHAR(120) NOT NULL,
  `password`   VARCHAR(200) NOT NULL,
  `is_admin`   TINYINT(1)   NOT NULL DEFAULT 0,
  `is_active`  TINYINT(1)   NOT NULL DEFAULT 1,
  `created_at` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_user_username` (`username`),
  UNIQUE KEY `uq_user_email`    (`email`)
);

-- Movies
CREATE TABLE IF NOT EXISTS `movies` (
  `id`           INT          NOT NULL AUTO_INCREMENT,
  `tmdb_id`      INT          NOT NULL,
  `title`        VARCHAR(200) NOT NULL,
  `overview`     TEXT,
  `release_date` VARCHAR(20),
  `poster_path`  VARCHAR(300),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_movies_tmdb_id` (`tmdb_id`)
);

-- Watchlist
CREATE TABLE IF NOT EXISTS `watchlist` (
  `id`          INT          NOT NULL AUTO_INCREMENT,
  `user_id`     INT          NOT NULL,
  `tmdb_id`     INT          NOT NULL,
  `title`       VARCHAR(200) NOT NULL,
  `poster_path` VARCHAR(300),
  `added_at`    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_movie` (`user_id`, `tmdb_id`),
  CONSTRAINT `fk_watchlist_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
);

-- Reviews
CREATE TABLE IF NOT EXISTS `reviews` (
  `id`         INT      NOT NULL AUTO_INCREMENT,
  `movie_id`   INT      NOT NULL,
  `user_id`    INT      NOT NULL,
  `rating`     INT,
  `comment`    TEXT,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_reviews_movie` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_reviews_user`  FOREIGN KEY (`user_id`)  REFERENCES `user`   (`id`) ON DELETE CASCADE
);
