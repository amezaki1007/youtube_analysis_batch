CREATE TABLE hidden (
  id INT NOT NULL AUTO_INCREMENT,
  video_id VARCHAR(20) NOT NULL,
  source_table ENUM('videos', 'recent_videos') NOT NULL,
  deleted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);
