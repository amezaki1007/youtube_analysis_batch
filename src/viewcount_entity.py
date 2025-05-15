from dataclasses import dataclass
from datetime import datetime, date

@dataclass
class ViewcountEntity:
  video_id: str
  view_count: int
  log_date: date

  @classmethod
  def from_json(cls, data: dict) -> "ViewcountEntity":
    statistics = data.get("statistics", {})
    video_id = data.get("id")
    view_count = int(statistics.get("viewCount"))
    log_date_raw = data.get("log_date")

    # log_date が datetime 型なら date に変換、それ以外ならそのまま使う
    if isinstance(log_date_raw, datetime):
      log_date = log_date_raw.date()
    elif isinstance(log_date_raw, date):
      log_date = log_date_raw
    else:
      # 文字列なら parse（必要に応じてフォーマット調整）
      log_date = datetime.fromisoformat(log_date_raw).date()

    return cls(
      video_id=video_id,
      view_count=view_count,
      log_date=log_date
    )
