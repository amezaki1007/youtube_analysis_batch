CREATE TABLE videos (
  id int NOT NULL AUTO_INCREMENT,
  video_id varchar(20) NOT NULL,
  title text,
  category_id varchar(10) DEFAULT NULL,
  channel_id varchar(50) DEFAULT NULL,
  channel_title varchar(255) DEFAULT NULL,
  description text,
  published_at datetime DEFAULT NULL,
  tags text,
  thumbnail_url text,
  video_type varchar(50) DEFAULT NULL,
  status varchar(10) DEFAULT NULL,
  hide tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY unique_title (title(255))
);