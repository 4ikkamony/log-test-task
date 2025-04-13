import re
from typing import Callable, Optional
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from enum import Enum

from tqdm import tqdm


# can be used to stop reading file after a certain amount of lines
LOOP_LIMIT: Optional[int] = None

BASE_DIR = Path(__name__).resolve().parent

LOG_FILE_NAME = "app_2.log"

LOG_FILE_PATH = BASE_DIR / LOG_FILE_NAME

ERROR_MESSAGES = {
    0: "Battery device error",
    1: "Temperature device error",
    2: "Threshold central error",
    3: "Unknown device error"
}


class InvalidLogMessageError(Exception):
    pass


class State(Enum):
    OK = "02"
    FAILED = "DD"


@dataclass
class ReportDTO:
    ok_counts_by_device_id: dict
    error_messages_by_device_id: dict

    total_big_count: int = 0
    total_ok_count: int = 0
    total_failed_count: int = 0


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


def _parse_message(line: str) -> tuple[str, str, str, State]:
    """"Excract HANDLER, ID, S_P_1, S_P_2 and STATE form log line"""
    match = re.search(LOG_PATTERN, line)

    if not match:
        raise InvalidLogMessageError(f"Could not match {line}")

    device_id = str(match.group(1))
    s_p_1 = (match.group(2))
    s_p_2 = (match.group(3))
    state = State(match.group(4))

    return device_id, s_p_1, s_p_2, state


def _get_error_messages(s_p_1: str, s_p_2: str) -> list[str]:
    """Process messages with STATUS=DD and figure out error messages"""
    s_p_1 = s_p_1[:-1] # get rid of control sum
    status_str = s_p_1 + s_p_2

    pairs = [status_str[i:i + 2] for i in range(0, len(status_str), 2)]

    # a flag is 4-th bit from the right of binary representation of a pair(8 bit total)
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


def _init_report_dto() -> ReportDTO:
    return ReportDTO(
        ok_counts_by_device_id = defaultdict(int),
        error_messages_by_device_id = defaultdict(list)
    )


def _get_report_from_logs(
    filepath: str | Path,
    loop_limit: int,
    report_initializer: Callable[..., ReportDTO],
) -> ReportDTO:
    """Goes through file line by line and writes data into a ReportDTO object"""

    report = report_initializer()

    with open(filepath, "r") as log_file:
        for i, line in enumerate(tqdm(log_file, desc="Processing logs")):
            if loop_limit and i > loop_limit:
                break

            if "BIG" not in line:
                continue

            report.total_big_count += 1

            try:
                device_id, s_p_1, s_p_2, state = _parse_message(line)
            except InvalidLogMessageError as exception:
                print(exception)
                continue

            if state == State.OK:
                report.total_ok_count += 1
                if device_id not in report.error_messages_by_device_id:
                    report.ok_counts_by_device_id[device_id] += 1
            else:
                report.total_failed_count += 1
                if device_id in report.ok_counts_by_device_id:
                    del report.ok_counts_by_device_id[device_id]

                error_messages = _get_error_messages(s_p_1, s_p_2)
                report.error_messages_by_device_id[device_id].extend(error_messages)
    return report


def _display_report(report: ReportDTO) -> None:
    print(f"{'=' * 36}Report{'=' * 36}")
    print(f"Total 'BIG' messages     : {report.total_big_count}")
    print(f"Successful messages   : {report.total_ok_count}")
    print(f"Failed messages       : {report.total_failed_count}")
    print()

    if report.error_messages_by_device_id:
        print("Errors per device:")
        for device_id, error_messages in report.error_messages_by_device_id.items():
            print(f"  {device_id}: {", ".join(error_messages)}")
        print()

    if report.ok_counts_by_device_id:
        print("Success messages count per device:")
        for device_id, count in report.ok_counts_by_device_id.items():
            print(f"  {device_id}: {count}")
        print()

    print("=" * 36)
    print(
        f"TOTAL OK DEVICES: {len(report.ok_counts_by_device_id)}"
        f" | "
        f"TOTAL FAILED DEVICES: {len(report.error_messages_by_device_id)}"
    )
    print("=" * 36)


def main(
    filepath: str | Path = LOG_FILE_PATH,
    loop_limit: Optional[int] = LOOP_LIMIT,
    report_initializer: Callable[..., ReportDTO] = _init_report_dto,
) -> None:
    report = _get_report_from_logs(
        filepath=filepath,
        loop_limit=loop_limit,
        report_initializer=report_initializer
    )

    _display_report(report)


if __name__ == "__main__":
    main()
