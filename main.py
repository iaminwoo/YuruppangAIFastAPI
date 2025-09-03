from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from youtube_api import extract_video_id, get_video_info
from youtube_captions import get_captions
from gemini import generate_by_gemini, validate_ingredients

app = FastAPI(title="YouTube Recipe Generator")


class VideoURL(BaseModel):
    youtube_url: str
    categories: str


@app.get("/")
async def root():
    return {"message": "YouTube Recipe Service Running"}


@app.post("/generate-recipe")
async def generate_recipe(data: VideoURL):
    video_id = extract_video_id(data.youtube_url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    video_info = await get_video_info(video_id)
    if not video_info:
        raise HTTPException(status_code=404, detail="Video not found")

    captions = get_captions(video_id)

    gemini_result = await generate_by_gemini(video_info, captions, data.youtube_url, data.categories)

    validate_ingredients(gemini_result)

    return gemini_result
