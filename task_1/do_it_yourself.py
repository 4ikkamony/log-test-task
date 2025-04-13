import re
from collections import defaultdict
from pathlib import Path
from enum import Enum


LOOP_LIMIT = 10


class State(Enum):
    OK = "02"
    FAILED = "DD"


BASE_DIR = Path(__name__).resolve().parent

LOG_FILE_NAME = "app_2.log"

LOG_FILE_PATH = BASE_DIR / LOG_FILE_NAME

ERROR_MESSAGES = {
    0: "Battery device error",
    1: "Temperature device error",
    2: "Threshold central error",
    3: "Unknown device error"
}

# captures groups:
#   1: ID
#   2: S_P_1
#   3: S_P_2
#   4: STATE
LOG_PATTERN = (
    r"'"
      r"BIG;"
      r"-?[0-9]+;"
      r"([0-9a-zA-Z]{6});" # ID
      r"(?:[0-9]+;){3}"
      r"(-?[0-9]{4});" # S_P_1
      r"(?:-?[0-9]+;){6}"
      r"(-?[0-9]{3});" # S_P_2
      r"(?:-?[0-9]+;){3}"
      r"(02|DD);" # STATE
    r"'")


def parse_message(line: str) -> tuple[str, str, str, State]:
    """"Excract HANDLER, ID, S_P_1, S_P_2 and STATE form log line"""
    match = re.search(LOG_PATTERN, line)
    print(match)
    device_id = str(match.group(1))
    s_p_1 = (match.group(2))
    s_p_2 = (match.group(3))
    state = State(match.group(4))

    return device_id, s_p_1, s_p_2, state


def get_error_messages(s_p_1: str, s_p_2: str) -> list[str]:
    """Process messages with STATUS=DD and figure out error messages"""
    s_p_1 = s_p_1[:-1] # get rid of control sum
    status_str = s_p_1 + s_p_2

    pairs = [status_str[i:i + 2] for i in range(0, len(status_str), 2)]

    # a flag is 4-th bit from the right of binary representation of a pair(8 bit total)
    print(status_str)
    flags: list[int] = [
        int(
            bin(int(pair))[2:].zfill(8)[4]
        )
        for pair in pairs
    ]

    error_messages = [
        ERROR_MESSAGES[i]
        for i, flag in enumerate(flags)
        if flag == 1
    ]

    return error_messages if error_messages else [ERROR_MESSAGES[3]]


def main(
    filepath: str | Path = LOG_FILE_PATH,
    limit: int = LOOP_LIMIT
):
    total_big_count: int = 0
    total_ok_count: int = 0
    total_failed_count: int = 0

    devices_ok_count = defaultdict(int)
    devices_errors = defaultdict(list)

    with open(filepath, "r") as log_file:
        for i, line in enumerate(log_file):
            if limit and i > limit:
                break

            if "BIG" not in line:
                continue

            total_big_count += 1

            device_id, s_p_1, s_p_2, state = parse_message(line)

            if state == State.OK:
                total_ok_count += 1
                if device_id not in devices_errors:
                    devices_ok_count[device_id] += 1
            else:
                total_failed_count += 1
                if device_id in devices_ok_count:
                    del devices_ok_count[device_id]

                error_messages = get_error_messages(s_p_1, s_p_2)
                devices_errors[device_id].extend(error_messages)

        print(devices_ok_count)
        print(devices_errors)

        print(total_big_count)
        print(total_ok_count)
        print(total_failed_count)


if __name__ == "__main__":
    main()
