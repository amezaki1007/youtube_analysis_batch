 CREATE TABLE viewcounts (
  id int NOT NULL AUTO_INCREMENT,
  video_id varchar(20) NOT NULL,
  view_count int NOT NULL,
  log_date date NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY unique_video_log (video_id,log_date)
)