import mysql.connector

from mysql_util import connect_to_database


def rotate_viewcounts(connection: mysql.connector.MySQLConnection):
  cursor = connection.cursor()
  delete_query = """
    DELETE FROM viewcounts 
    WHERE log_date < DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
  """
  cursor.execute(delete_query)
  connection.commit()
  print(f"{cursor.rowcount}件のレコードが削除されました")

def rotate_videos(connection: mysql.connector.MySQLConnection):
  cursor = connection.cursor()
  update_query = """
    UPDATE videos 
    SET status = 'DOWN' 
    WHERE published_at < DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
  """
  cursor.execute(update_query)
  connection.commit()
  print(f"{cursor.rowcount}件の動画のステータスがDOWNに更新されました")

def rotate_recent_videos(connection: mysql.connector.MySQLConnection):
  cursor = connection.cursor()
  update_query = """
    UPDATE recent_videos 
    SET status = 'DOWN' 
    WHERE published_at < DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
  """
  cursor.execute(update_query)
  connection.commit()
  print(f"{cursor.rowcount}件の動画のステータスがDOWNに更新されました")


if __name__ == '__main__':
  connection = connect_to_database()
  rotate_videos(connection)
  rotate_recent_videos(connection)
  rotate_viewcounts(connection)
