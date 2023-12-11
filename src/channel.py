import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    __api_key: str = os.getenv('YT_API_KEY', "AIzaSyDvOyF4Jtqcbovz26tMtBTkqYbUCGeTHeE")
    __youtube = build('youtube', 'v3', developerKey=__api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = Channel.__youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        info = json.loads(json.dumps(channel, indent=2, ensure_ascii=False))
        self.__title = info['items'][0]['snippet']['title']
        self.__description = info['items'][0]['snippet']['description']
        self.__url = 'https://www.youtube.com/channel/' + self.__channel_id
        self.__subscribers = int(info['items'][0]['statistics']['subscriberCount'])
        self.__video_count = int(info['items'][0]['statistics']['videoCount'])
        self.__view_count = int(info['items'][0]['statistics']['viewCount'])

    def __str__(self):
        return f"{self.__title} ({self.__url})"

    def __add__(self, other):
        return self.__subscribers + other.__subscribers

    def __sub__(self, other):
        return self.__subscribers - other.__subscribers

    def __eq__(self, other):
        return self.__subscribers == other.__subscribers

    def __lt__(self, other):
        return self.__subscribers < other.__subscribers

    def __le__(self, other):
        return self.__subscribers <= other.__subscribers

    def __gt__(self, other):
        return self.__subscribers > other.__subscribers

    def __ge__(self, other):
        return self.__subscribers >= other.__subscribers

    @property
    def title(self):
        return self.__title

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, new_channel_id):
        print("AttributeError: property 'channel_id' of 'Channel' object has no setter")

    @property
    def description(self):
        return self.__description

    @property
    def url(self):
        return self.__url

    @property
    def subscribers(self):
        return self.__subscribers

    @property
    def video_count(self):
        return self.__video_count

    @property
    def view_count(self):
        return self.__view_count

    @classmethod
    def get_service(cls):
        return cls.__youtube

    def to_json(self, file_name):
        data = {
            'channel_id': self.__channel_id,
            'title': self.__title,
            'description': self.__description,
            'url': self.__url,
            'subscribers': self.__subscribers,
            'video_count': self.__video_count,
            'view_count': self.__view_count
        }
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.__youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))
