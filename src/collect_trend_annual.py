# 直近三年の歌ってみた/ボカロオリジナルを再生回数が多い順に三か月刻みで取得
# 各シーズンごとに250件ずつ
from datetime import datetime

from request_api import ApiRequest
from video_entity import VideoEntity
from mysql_util import insert_video_entity_many
from util import get_api_key, get_season_datetime

if __name__ == "__main__":
  num_collect_uta = 200
  num_collect_ori = 450
  target_year = datetime.now().year - 3
  api_key = get_api_key(env_name="ANNUAL_API_KEY")
  api_request = ApiRequest(api_key)
  date_begin, date_end = get_season_datetime(target_year, 'spring')
  params = {
    'q': 'ボカロ',
    'publishedBefore': date_end,
    'publishedAfter': date_begin,
  }
  res_json_list = api_request.search(num=num_collect_ori, **params)
  video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  insert_video_entity_many(video_entities, table_name='videos')

  params = {
    'q': '歌ってみた',
    'publishedBefore': date_end,
    'publishedAfter': date_begin,
  }
  res_json_list = api_request.search(num=num_collect_uta, **params)
  video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  insert_video_entity_many(video_entities, table_name='videos')

  date_begin, date_end = get_season_datetime(target_year, 'summer')
  params = {
    'q': 'ボカロ',
    'publishedBefore': date_end,
    'publishedAfter': date_begin,
  }
  res_json_list = api_request.search(num=num_collect_ori, **params)
  video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  insert_video_entity_many(video_entities, table_name='videos')

  params = {
    'q': '歌ってみた',
    'publishedBefore': date_end,
    'publishedAfter': date_begin,
  }
  res_json_list = api_request.search(num=num_collect_uta, **params)
  video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  insert_video_entity_many(video_entities, table_name='videos')

  date_begin, date_end = get_season_datetime(target_year, 'fall')
  params = {
    'q': 'ボカロ',
    'publishedBefore': date_end,
    'publishedAfter': date_begin,
  }
  res_json_list = api_request.search(num=num_collect_ori, **params)
  video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  insert_video_entity_many(video_entities, table_name='videos')

  params = {
    'q': '歌ってみた',
    'publishedBefore': date_end,
    'publishedAfter': date_begin,
  }
  res_json_list = api_request.search(num=num_collect_uta, **params)
  video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  insert_video_entity_many(video_entities, table_name='videos')

  date_begin, date_end = get_season_datetime(target_year, 'winter')
  params = {
    'q': 'ボカロ',
    'publishedBefore': date_end,
    'publishedAfter': date_begin,
  }
  res_json_list = api_request.search(num=num_collect_ori, **params)
  video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  insert_video_entity_many(video_entities, table_name='videos')

  params = {
    'q': '歌ってみた',
    'publishedBefore': date_end,
    'publishedAfter': date_begin,
  }
  res_json_list = api_request.search(num=num_collect_uta, **params)
  video_entities = [VideoEntity.from_json(res_json) for res_json in res_json_list]
  insert_video_entity_many(video_entities, table_name='videos')
