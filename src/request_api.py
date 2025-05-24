from datetime import datetime, timezone

import requests

from util import filter_videos_by_duration


API_BASE_URL = 'https://youtube.googleapis.com/youtube/v3'

class ApiRequest:
  def __init__(self, api_key: str):
    self.api_key = api_key

  def video_viewcount(self, video_id_list: list):
    ret = []
    max_results = min(len(video_id_list), 50)
    params = {
      'part': 'statistics',
      'key': self.api_key,
      'maxResults': max_results,
      'relevanceLanguage': 'ja',
    }
    num_loop = (len(video_id_list) + max_results - 1) // max_results
    for i in range(num_loop):
      target = video_id_list[i*max_results:(i+1)*max_results]
      params.update({
        'id': ','.join(target),
      })
      result = requests.get(url=f'{API_BASE_URL}/videos', params=params)
      ret += result.json()['items']
    for item in ret:
      item.update({
        'log_date': datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).date()
      })
    return ret

  def videos(self, video_id_list: list, filter_short=True):
    params = {
      'part': 'snippet,contentDetails',
      'id': ','.join(video_id_list),
      'key': self.api_key,
      'maxResults': 50,
    }
    result = requests.get(url=f'{API_BASE_URL}/videos', params=params)
    if filter_short:
      return filter_videos_by_duration(result.json()['items'])
    else:
      return result.json()['items']

  def search(self, num, **kwargs):
    ret = []
    max_results = min(num, 50)
    num_page = (num + max_results - 1) // max_results
    kwargs.update({
      'part': 'snippet',
      'key': self.api_key,
      'type': 'video',
      'order': 'relevance',
      'maxResults': max_results,
    })
    next_page_token = ''
    for i in range(num_page):
      if next_page_token == 'END':
        break
      print(f"getting page {i}")
      if next_page_token != '':
        kwargs.update({
          'pageToken': next_page_token
        })
      result = requests.get(url=f'{API_BASE_URL}/search', params=kwargs)
      search_results = result.json()['items']
      try:
        next_page_token = result.json()['nextPageToken']
      except Exception as e:
        print("[WARNING]: ", e)
        print("there might be not enough search result.")
        next_page_token = 'END'
      # 追加で欲しい情報（タグなど）を取得
      try:
        video_id_list = [ item['id']['videoId'] for item in search_results if 'videoId' in item.get('id', {})]
      except Exception as e:
        print("response error: ", e)
        print("search list: ", search_results)
      ret += self.videos(video_id_list)
    for item in ret:
      item.update({
        'video_type': '歌ってみた' if '歌ってみた' in kwargs['q'] else 'ボカロオリジナル'
      })
    return ret
