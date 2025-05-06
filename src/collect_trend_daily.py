# 直近半年の歌ってみた/ボカロオリジナルを再生回数が多い順に取得
# 1000件ずつ
# 新着動画の歌ってみた/ボカロオリジナルを再生回数が多い順に取得
# 500件ずつ

from request_api import ApiRequest
from video_entity import VideoEntity
from mysql_util import insert_video_entity_many
from util import get_api_key, get_past_datetime

if __name__ == "__main__":
  api_key = get_api_key(is_env=True)
  api_request = ApiRequest(api_key)
  params = {
    'q': 'ボカロオリジナル',
    'publishedBefore': get_past_datetime(0),
    'publishedAfter': get_past_datetime(180),
  }
  res_json_list = api_request.search(num=5, **params)
  video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  insert_video_entity_many(video_entities, table_name='videos')

  params = {
    'q': '歌ってみた',
    'publishedBefore': get_past_datetime(0),
    'publishedAfter': get_past_datetime(180),
  }
  res_json_list = api_request.search(num=5, **params)
  video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  print(video_entities)
  insert_video_entity_many(video_entities, table_name='videos')

  # params = {
  #   'q': 'ボカロオリジナル',
  #   'publishedBefore': get_past_datetime(0),
  #   'publishedAfter': get_past_datetime(7),
  # }
  # res_json_list = api_request.search(num=5, **params)
  # video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  # insert_video_entity_many(video_entities, table_name='recent_videos')

  # params = {
  #   'q': '歌ってみた',
  #   'publishedBefore': get_past_datetime(0),
  #   'publishedAfter': get_past_datetime(7),
  # }
  # res_json_list = api_request.search(num=5, **params)
  # video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  # insert_video_entity_many(video_entities, table_name='recent_videos')