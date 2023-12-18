import json
import os
from googleapiclient.discovery import build


class Video:
    __api_key: str = os.getenv('YT_API_KEY', "AIzaSyDvOyF4Jtqcbovz26tMtBTkqYbUCGeTHeE")
    __youtube = build('youtube', 'v3', developerKey=__api_key)

    def __init__(self, video_id):
        self.video_id = video_id
        video = Video.__youtube.videos().list(part="snippet,statistics", id=video_id).execute()
        info = json.loads(json.dumps(video, indent=2, ensure_ascii=False))
        self.title = info['items'][0]['snippet']['title']
        self.url = "https://www.youtube.com/watch?v=" + info['items'][0]['id']
        self.view_count = info['items'][0]['statistics']['viewCount']
        self.like_count = info['items'][0]['statistics']['likeCount']


    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
