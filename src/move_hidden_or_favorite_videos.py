# パフォーマンス向上のため非表示にした動画を物理的に別テーブルに移動させる

from mysql_util import connect_to_database


def move_hidden_videos(connection) -> list[str]:
    """
    videos および recent_videos テーブルから video_id をすべて取得してリストで返す
    """
    cursor = connection.cursor()
    
    try:
        for table in ["videos", "recent_videos"]:
            cursor.execute(f"SELECT video_id, '{table}' AS source_table FROM {table} where hide = 1")
            rows = cursor.fetchall()

            for video_id, source_table in rows:
                cursor.execute("INSERT INTO hidden (video_id, source_table) VALUES (%s, %s)",
                               (video_id, source_table))
                
            cursor.execute(f"DELETE FROM {table} where hide = 1")
            delete_count = cursor.rowcount
            print(f'{delete_count}件の非表示リストが{table}テーブルからhiddenテーブルに移動しました')
        connection.commit()

    finally:
        cursor.close()


if __name__ == "__main__":
  mysql_conn = connect_to_database()
  video_ids = move_hidden_videos(mysql_conn)
  