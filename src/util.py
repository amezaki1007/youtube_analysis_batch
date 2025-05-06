import os
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

def get_api_key(file='', is_env=False):
  if is_env:
    return os.getenv('YOUTUBE_API_KEY')
  with open(file) as f:
    return f.read().strip()

def get_past_datetime(days):
  target_date = datetime.now(timezone.utc) - relativedelta(days=days)
  return target_date.strftime("%Y-%m-%dT%H:%M:%SZ")

def get_season_datetime(year: int, season: str):
  """指定した年と季節（spring/summer/fall/winter）に対応する
  ISO 8601（Z付き・秒まで）形式の開始・終了日時を返す"""

  season = season.lower()
  if season == "spring":
      start = datetime(year, 3, 1, 0, 0, 0, tzinfo=timezone.utc)
      end = datetime(year, 5, 31, 23, 59, 59, tzinfo=timezone.utc)
  elif season == "summer":
      start = datetime(year, 6, 1, 0, 0, 0, tzinfo=timezone.utc)
      end = datetime(year, 8, 31, 23, 59, 59, tzinfo=timezone.utc)
  elif season == "fall":
      start = datetime(year, 9, 1, 0, 0, 0, tzinfo=timezone.utc)
      end = datetime(year, 11, 30, 23, 59, 59, tzinfo=timezone.utc)
  elif season == "winter":
      start = datetime(year, 12, 1, 0, 0, 0, tzinfo=timezone.utc)
      end = datetime(year + 1, 2, 28, 23, 59, 59, tzinfo=timezone.utc)  # 閏年対応は簡略化
  else:
      raise ValueError("season must be one of: spring, summer, fall, winter")

  # ミリ秒なしの ISO 8601 + Z 形式に変換
  fmt = "%Y-%m-%dT%H:%M:%SZ"
  return start.strftime(fmt), end.strftime(fmt)