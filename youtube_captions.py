from youtube_transcript_api import YouTubeTranscriptApi


def get_captions(video_id: str):
    ytt_api = YouTubeTranscriptApi()
    fetched_transcript = ytt_api.fetch(video_id, languages=['ko', 'en'])

    full_text = " ".join([snippet.text for snippet in fetched_transcript])
    return full_text


if __name__ == "__main__":
    vid = "5RP8S8LPOwM"
    print(get_captions(vid))
