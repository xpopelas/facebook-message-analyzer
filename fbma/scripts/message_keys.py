"""Gets tree of arguments in facebook messages.

Provide argument to this script (any argument) to show debug logs.
"""

import json
import logging
import os
import sys
import time
from typing import Set


def find_all_files_with_suffix(source: str, suffix: str) -> Set[str]:
    suffix = suffix.lower()
    result = set()
    for (dir_path, _, filenames) in os.walk(source):
        for file in filenames:
            if file.lower().endswith(suffix):
                result.add(f"{dir_path}/{file}")
    return result


def load_json_from_file(path: str):
    with open(path, "r", encoding="UTF-8") as fh:
        return json.load(fh)


def analyze_dict(fb_dict: dict) -> set:
    result = set()
    for key, value in fb_dict.items():
        if isinstance(value, dict):
            further = analyze_dict(value)
            for v in further:
                result.add(f"{key}->{v}")
        elif isinstance(value, list):
            for el in value:
                if isinstance(el, dict):
                    further = analyze_dict(el)
                    for v in further:
                        result.add(f"{key}->{v}")
                else:
                    result.add(f"{key}->({type(el)})")
        else:
            result.add(f"{key}->({type(value)})")
    return result


def main():
    logging.basicConfig(
        level=logging.DEBUG if len(sys.argv) > 1 else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    time_before = time.perf_counter()
    fb_dicts = []
    inbox_path = "../../.fbdata/messages/inbox"
    paths = find_all_files_with_suffix(inbox_path, ".json")
    for path in paths:
        fb_dicts.append(load_json_from_file(path))
    logging.debug("Successfully loaded all %d fb_dicts", len(fb_dicts))
    analyzed = set()
    for fb_dict in fb_dicts:
        analyzed = analyzed.union(analyze_dict(fb_dict))
    logging.debug("Successfully analyzed all dicts")
    print("Tree of paths")
    for item in sorted(analyzed):
        print(item)
    time_after = time.perf_counter()
    logging.debug("This script ran for %.3fs", time_after - time_before)


if __name__ == "__main__":
    main()
