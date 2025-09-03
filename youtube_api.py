import os
from dotenv import load_dotenv
import httpx
from urllib.parse import urlparse, parse_qs

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def extract_video_id(youtube_url: str) -> str:
    # 유튜브 URL 에서 video_id 추출
    parsed_url = urlparse(youtube_url)

    # youtu.be 단축 URL
    if parsed_url.hostname in ["youtu.be"]:
        video_id = parsed_url.path[1:]  # /VIDEO_ID
        if "?" in video_id:
            video_id = video_id.split("?")[0]  # ? 뒤 제거
        return video_id

    # 일반 youtube.com URL
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        query = parse_qs(parsed_url.query)
        return query.get("v", [None])[0]

    return ""


async def get_video_info(video_id: str):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YOUTUBE_API_KEY}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        if not data.get("items"):
            return None
        snippet = data["items"][0]["snippet"]
        return {
            "title": snippet["title"],
            "description": snippet["description"],
            "channel": snippet["channelTitle"]
        }
