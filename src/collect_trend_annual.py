# 直近三年の歌ってみた/ボカロオリジナルを再生回数が多い順に三か月刻みで取得
# 各シーズンごとに250件ずつ
from request_api import ApiRequest
from video_entity import VideoEntity
from mysql_util import insert_video_entity_many
from util import get_api_key, get_season_datetime

if __name__ == "__main__":
  api_key = get_api_key(is_env=True)
  api_request = ApiRequest(api_key)
  date_begin, date_end = get_season_datetime(2022, 'spring')
  params = {
    'q': 'ボカロオリジナル',
    'publishedBefore': date_begin,
    'publishedAfter': date_end,
  }
  res_json_list = api_request.search(num=5, **params)
  video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  insert_video_entity_many(video_entities, table_name='videos')

  params = {
    'q': '歌ってみた',
    'publishedBefore': date_begin,
    'publishedAfter': date_end,
  }
  res_json_list = api_request.search(num=5, **params)
  video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  insert_video_entity_many(video_entities, table_name='videos')

  date_begin, date_end = get_season_datetime(2022, 'summer')
  params = {
    'q': 'ボカロオリジナル',
    'publishedBefore': date_begin,
    'publishedAfter': date_end,
  }
  res_json_list = api_request.search(num=5, **params)
  video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  insert_video_entity_many(video_entities, table_name='videos')

  params = {
    'q': '歌ってみた',
    'publishedBefore': date_begin,
    'publishedAfter': date_end,
  }
  res_json_list = api_request.search(num=5, **params)
  video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  insert_video_entity_many(video_entities, table_name='videos')

  date_begin, date_end = get_season_datetime(2022, 'fall')
  params = {
    'q': 'ボカロオリジナル',
    'publishedBefore': date_begin,
    'publishedAfter': date_end,
  }
  res_json_list = api_request.search(num=5, **params)
  video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  insert_video_entity_many(video_entities, table_name='videos')

  params = {
    'q': '歌ってみた',
    'publishedBefore': date_begin,
    'publishedAfter': date_end,
  }
  res_json_list = api_request.search(num=5, **params)
  video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  insert_video_entity_many(video_entities, table_name='videos')

  date_begin, date_end = get_season_datetime(2022, 'winter')
  params = {
    'q': 'ボカロオリジナル',
    'publishedBefore': date_begin,
    'publishedAfter': date_end,
  }
  res_json_list = api_request.search(num=5, **params)
  video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  insert_video_entity_many(video_entities, table_name='videos')

  params = {
    'q': '歌ってみた',
    'publishedBefore': date_begin,
    'publishedAfter': date_end,
  }
  res_json_list = api_request.search(num=5, **params)
  video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  insert_video_entity_many(video_entities, table_name='videos')