import pytest

from fbma.messages.chat_loading import ChatLoader


@pytest.mark.usefixtures("fake_fbdata_path")
def test_chat_loader(fake_fbdata_path):
    loader = ChatLoader(fake_fbdata_path)

    # check chats are empty
    assert not loader.archived
    assert not loader.filtered
    assert not loader.inbox

    loader.load_chats()

    # check if loaded chats actually loaded
    assert loader.archived
    assert loader.filtered
    assert loader.inbox

