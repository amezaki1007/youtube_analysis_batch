# videosとrecent_videosに入っているvideoIdのviewCount取得

from request_api import ApiRequest
from viewcount_entity import ViewcountEntity
from mysql_util import connect_to_database, insert_viewcount_entity_many
from util import get_api_key


def get_all_video_ids(connection) -> list[str]:
    """
    videos および recent_videos テーブルから video_id をすべて取得してリストで返す
    """
    video_ids = []
    cursor = connection.cursor()
    
    try:
        for table in ["videos", "recent_videos"]:
            cursor.execute(f"SELECT video_id FROM {table}")
            rows = cursor.fetchall()
            video_ids.extend([row[0] for row in rows])
    finally:
        cursor.close()

    return video_ids


if __name__ == "__main__":
  mysql_conn = connect_to_database()
  video_ids = get_all_video_ids(mysql_conn)

  api_key = get_api_key(is_env=True)
  api_request = ApiRequest(api_key)
  res_json_list = api_request.video_viewcount(video_ids)
  viewcount_entities = [ViewcountEntity.from_json(res_json) for res_json in res_json_list]
  print(viewcount_entities)
  insert_viewcount_entity_many(viewcount_entities, table_name='viewcounts')
  