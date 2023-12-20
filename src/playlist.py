import json
import os
from googleapiclient.discovery import build
from datetime import timedelta


class PlayList:
    __api_key: str = os.getenv('YT_API_KEY', "AIzaSyDvOyF4Jtqcbovz26tMtBTkqYbUCGeTHeE")
    __youtube = build('youtube', 'v3', developerKey=__api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlist = PlayList.__youtube.playlists().list(part='snippet', id=playlist_id).execute()
        playlist_items = PlayList.__youtube.playlistItems().list(part='contentDetails',
                                                                 playlistId=playlist_id).execute()
        info = json.loads(json.dumps(playlist, indent=2, ensure_ascii=False))
        info2 = json.loads(json.dumps(playlist_items, indent=2, ensure_ascii=False))
        self.title = info['items'][0]['snippet']['title']
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id
        videos_duration = []
        self.__best_video_id = ""
        like_count = 0
        for video in info2['items']:
            v = PlayList.__youtube.videos().list(part='contentDetails,statistics',
                                                 id=video['contentDetails']['videoId']).execute()
            info3 = json.loads(json.dumps(v, indent=2, ensure_ascii=False))
            videos_duration.append(info3['items'][0]['contentDetails']['duration'])
            if like_count <= int(info3['items'][0]['statistics']['likeCount']):
                self.__best_video_id = info3['items'][0]['id']
        self.__total_duration = timedelta(seconds=0, minutes=0, hours=0)

        for duration in videos_duration:
            hour = 0
            minute = 0
            second = 0
            curr = 2
            for i in range(2, len(duration)):
                if duration[i] == 'H':
                    hour = int(duration[curr:i])
                    curr = i + 1
                if duration[i] == 'M':
                    minute = int(duration[curr:i])
                    curr = i + 1
                if duration[i] == 'S':
                    second = int(duration[curr:i])
                    curr = i + 1
            video_duration = timedelta(seconds=second, minutes=minute, hours=hour)
            self.__total_duration += video_duration

    @property
    def total_duration(self):
        return self.__total_duration

    def show_best_video(self):
        return "https://youtu.be/" + self.__best_video_id
