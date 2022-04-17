import json
import os
from pathlib import Path
from typing import List, Set

from fbma.messages.models import FbChat


class ChatLoader:
    source: Path = Path(".fbdata")
    archived: List[FbChat]
    filtered: List[FbChat]
    inbox: List[FbChat]
    message_requests: List[FbChat]

    def __init__(self, source: Path | None = None):
        if source is not None:
            self.source = source

        self.archived = []
        self.filtered = []
        self.inbox = []
        self.message_requests = []

    def load_chats(self):
        categories = [
            ("archived_threads", self.archived),
            ("filtered_threads", self.filtered),
            ("inbox", self.inbox),
            ("message_requests", self.message_requests),
        ]
        msg_path = Path("messages")

        chat_files = []
        filepaths = self.find_all_jsons(msg_path)
        for filepath in filepaths:
            content = self.load_json(filepath)
            chat_files.append(FbChat(content))

        thread_paths = {
            chat.thread_path for chat in chat_files if chat.thread_path is not None
        }
        for tp in thread_paths:
            chats = sorted(
                filter(lambda c1, e=tp: c1.thread_path == e, chat_files),
                key=lambda c2: c2.messages[0].timestamp_ms
                if c2.messages
                else float("inf"),
            )
            chat = chats[0]
            for c in chats[1:]:
                chat.merge(c)
            for thread, group in categories:
                if chat.thread_path.startswith(thread):
                    group.append(chat)

    def find_all_jsons(self, additional_source: Path | None) -> Set[Path]:
        source = self.source
        if source is not None:
            source /= additional_source

        result: Set[Path] = set()
        for (dir_path, _, filenames) in os.walk(source):
            for file in filenames:
                if file.lower().endswith(".json"):
                    result.add(Path(dir_path) / Path(file))

        return result

    @staticmethod
    def load_json(source: Path) -> dict | list | str | None:
        with open(source, "r", encoding="UTF-8") as fh:
            return json.load(fh)
