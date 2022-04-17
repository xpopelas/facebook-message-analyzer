"""Script for checking time efficiency.

This script will load the entire Facebook messages directory.
For this script to work, have your data in `.fbdata` folder.
"""
import logging
import sys
import time

from messages.chat_loading import ChatLoader


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    loader = ChatLoader()
    perf_time_before = time.perf_counter()
    logging.debug("Started loading of chat.")
    loader.load_chats()
    logging.debug("Loading finished.")
    perf_time_after = time.perf_counter()
    logging.debug("Perf time: %.3fs.", perf_time_after - perf_time_before)


if __name__ == "__main__":
    main()
