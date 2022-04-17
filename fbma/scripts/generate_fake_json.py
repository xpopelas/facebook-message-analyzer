import json
import os
import random
from pathlib import Path
from typing import List


def generate_messages(count: int | None = None, user1: str | None = None, user2: str | None = None) -> List[List[dict]]:
    if count is None:
        count = random.randint(500, 9000)

    if user1 is None:
        user1 = "Test User 1"

    if user2 is None:
        user2 = "Test User 2"

    result = []
    timestamp = 123_456_789_012 + random.randint(-10_000_000, 10_000_000)
    current_chat = None
    for msg_i in range(count):
        if msg_i % 10_000 == 0:
            if current_chat is not None:
                result.append(current_chat)
            current_chat = []

        user = random.choice([user1, user2])
        msg = {
            "sender_name": user,
            "timestamp_ms": timestamp,
            "content": f"Test message {msg_i + 1}",
            "type": "Generic",
            "is_unsent": False,
        }
        current_chat.append(msg)

        timestamp += random.randint(100, 50_000)

    result.append(current_chat)
    return result


def generate_chats(msg_count: int | None = None, user1: str | None = None, user2: str | None = None, category: str | None = None) -> List[dict]:
    if msg_count is None:
        msg_count = random.randint(500, 9000)

    if user1 is None:
        user1 = "Test User 1"

    if user2 is None:
        user2 = "Test User 2"

    if category is None:
        category = "inbox"

    result = []
    thread_path = f"{category.lower()}/{user1.lower().replace(' ', '')}_{hex(random.randint(1_000_000, 100_000_000))[2:]}"
    messages_lists = generate_messages(msg_count, user1, user2)
    for messages in messages_lists:
        chat = {
            "participants": [
                {
                    "name": user1,
                },
                {
                    "name": user2,
                },
            ],
            "messages": messages,
            "title": user1,
            "is_still_participant": True,
            "thread_type": "Regular",
            "thread_path": thread_path,
            "magic_words": []
        }
        result.append(chat)
    return result


def main():
    count = random.randint(34_000, 55_000)
    user1 = "Chat Bot"
    user2 = "Test User"
    category = "archived_threads"
    path = Path("generated_files")
    chats = generate_chats(count, user1, user2, category)

    dir_name = chats[0]["thread_path"].split('/')[-1]
    path /= Path(dir_name)
    os.mkdir(path)
    for count, chat in enumerate(chats):
        with open(path / Path(f"message_{count + 1}.json"), "w") as fh:
            fh.write(json.dumps(chat, indent=2))


if __name__ == "__main__":
    main()
