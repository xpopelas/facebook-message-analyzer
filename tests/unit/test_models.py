import pytest

from fbma.messages.models import FbChat


@pytest.mark.usefixtures("simple_message_dict")
def test_chat_sample_simple(simple_message_dict):
    fb_chat = FbChat(simple_message_dict)
    assert len(fb_chat.participants) == 2
    assert len(fb_chat.messages) == 4
    assert fb_chat.messages == sorted(
        fb_chat.messages, key=lambda msg: msg.timestamp_ms
    )
    assert fb_chat.participants[0].name in ("Participant", "User")
    assert fb_chat.participants[1].name in ("Participant", "User")
    assert fb_chat.participants[0] != fb_chat.participants[1]
