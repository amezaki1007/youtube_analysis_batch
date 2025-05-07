from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class VideoEntity:
  video_id: str
  title: str
  category_id: Optional[str]
  channel_id: str
  channel_title: str
  description: str
  published_at: datetime
  tags: str
  thumbnail_url: str
  video_type: str
  status: str

  @classmethod
  def from_json(cls, data: dict) -> "VideoEntity":
    snippet = data.get("snippet", {})
    video_id = data.get("id")
    title = snippet.get("title", "")
    category_id = snippet.get("categoryId")
    channel_id = snippet.get("channelId", "")
    channel_title = snippet.get("channelTitle", "")
    description = snippet.get("description", "")
    published_at_raw = snippet.get("publishedAt", "")
    tags_list = snippet.get("tags", [])
    tags = ",".join(tags_list)

    # 最適なサムネイル選択
    thumbnails = snippet.get("thumbnails", {})
    thumbnail_url = (
      thumbnails.get("maxres")
      or thumbnails.get("standard")
      or thumbnails.get("high")
      or {}
    ).get("url", "")

    video_type = data.get("video_type")

    # ISO 8601 -> datetime に変換
    published_at = datetime.fromisoformat(published_at_raw.replace("Z", "+00:00"))

    return cls(
      video_id=video_id,
      title=title,
      category_id=category_id,
      channel_id=channel_id,
      channel_title=channel_title,
      description=description,
      published_at=published_at,
      tags=tags,
      thumbnail_url=thumbnail_url,
      video_type=video_type,
      status="UP"
    )