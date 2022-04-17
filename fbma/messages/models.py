import dataclasses
from typing import List


@dataclasses.dataclass
class FbUri:
    uri: str

    def __init__(self, dct: dict):
        self.uri = dct.get("uri")


@dataclasses.dataclass
class FbUser:
    name: str

    def __init__(self, dct: dict):
        self.name = dct.get("name")


@dataclasses.dataclass
class FbFile:
    creation_timestamp: int
    uri: str

    def __init__(self, dct: dict):
        self.creation_timestamp = dct.get("creation_timestamp")
        self.uri = dct.get("uri")


@dataclasses.dataclass
class FbVideo:
    creation_timestamp: int
    thumbnail: FbUri
    uri: FbUri

    def __init__(self, dct: dict):
        self.creation_timestamp = dct.get("creation_timestamp")
        self.thumbnail = FbUri(dct.get("thumbnail"))
        self.uri = FbUri(dct)


@dataclasses.dataclass
class FbReaction:
    actor: str
    reaction: str

    def __init__(self, dct: dict):
        self.actor = dct.get("actor")
        self.reaction = dct.get("reaction")


@dataclasses.dataclass
class FbShare:
    link: str
    share_text: str

    def __init__(self, dct: dict):
        self.link = dct.get("link")
        self.share_text = dct.get("share_text")


@dataclasses.dataclass
class FbMessage:  # pylint: disable=too-many-locals
    sender_name: str = None
    timestamp_ms: int = None
    type: str | None = None
    content: str | None = None
    is_unsent: bool = None
    ip: str | None = None

    reactions: List[FbReaction] | None = None
    photos: List[FbFile] | None = None
    gifs: List[FbUri] | None = None
    videos: List[FbVideo] | None = None
    share: FbShare | None = None
    sticker: FbUri | None = None
    audio_files: List[FbFile] | None = None
    files: List[FbFile] | None = None

    users: List[FbUser] | None = None

    call_duration: int | None = None
    missed: bool | None = None

    def __init__(self, message_dict: dict):  # pylint: disable=too-many-branches
        self.sender_name = message_dict.get("sender_name")
        self.timestamp_ms = message_dict.get("timestamp_ms")
        self.type = message_dict.get("type")
        self.content = message_dict.get("content")
        self.is_unsent = message_dict.get("is_unsent")
        self.ip = message_dict.get("ip")

        self.call_duration = message_dict.get("call_duration")
        self.missed = message_dict.get("missed")

        if (reactions := message_dict.get("reactions")) is not None:
            self.reactions = []
            for react in reactions:
                self.reactions.append(FbReaction(react))
        if (photos := message_dict.get("photos")) is not None:
            self.photos = []
            for photo in photos:
                self.photos.append(FbFile(photo))
        if (gifs := message_dict.get("gifs")) is not None:
            self.gifs = []
            for gif in gifs:
                self.gifs.append(FbUri(gif))
        if (videos := message_dict.get("videos")) is not None:
            self.videos = []
            for video in videos:
                self.videos.append(FbVideo(video))
        if (share := message_dict.get("share")) is not None:
            self.share = FbShare(share)
        if (sticker := message_dict.get("sticker")) is not None:
            self.sticker = FbUri(sticker)
        if (audio_files := message_dict.get("audio_files")) is not None:
            self.audio_files = []
            for audio_file in audio_files:
                self.audio_files.append(FbFile(audio_file))
        if (files := message_dict.get("files")) is not None:
            self.files = []
            for file in files:
                self.files.append(FbFile(file))
        if (users := message_dict.get("users")) is not None:
            self.users = []
            for file in users:
                self.users.append(FbUser(file))


@dataclasses.dataclass
class FbJoinableMode:
    link: str
    mode: int

    def __init__(self, dct: dict):
        self.link = dct.get("link")
        self.mode = dct.get("mode")


@dataclasses.dataclass
class FbChat:
    title: str | None = None
    thread_type: str | None = None
    thread_path: str | None = None
    participants: List[FbUser] | None = None
    is_still_participant: bool | None = None
    image: FbFile | None = None
    joinable_mode: FbJoinableMode | None = None
    messages: List[FbMessage] | None = None

    def __init__(self, dct: dict):
        self.title = dct.get("title")
        self.thread_type = dct.get("thread_type")
        self.thread_path = dct.get("thread_path")
        if (participants := dct.get("participants")) is not None:
            self.participants = []
            for participant in participants:
                self.participants.append(FbUser(participant))
        self.is_still_participant = dct.get("is_still_participant")
        if (image := dct.get("image")) is not None:
            self.image = FbFile(image)
        if (joinable_mode := dct.get("joinable_mode")) is not None:
            self.joinable_mode = FbJoinableMode(joinable_mode)
        self.messages = []
        if (messages := dct.get("messages")) is not None:
            for message in messages:
                self.messages.append(FbMessage(message))
        self.messages.sort(key=lambda msg: msg.timestamp_ms)

    def merge(self, other: "FbChat") -> "FbChat":
        if self.title == other.title and self.thread_path == other.thread_path:
            self.messages += other.messages
            self.messages.sort(key=lambda x: x.timestamp_ms)
        return self
