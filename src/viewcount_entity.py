from dataclasses import dataclass
from datetime import datetime

@dataclass
class ViewcountEntity:
  video_id: str
  view_count: int
  log_date: datetime

  @classmethod
  def from_json(cls, data: dict) -> "ViewcountEntity":
    statistics = data.get("statistics", {})
    video_id = data.get("id")
    view_count = int(statistics.get("viewCount"))
    log_date = data.get("log_date")

    return cls(
      video_id=video_id,
      view_count=view_count,
      log_date=log_date
    )
