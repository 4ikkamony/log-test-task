import re
from pathlib import Path


BASE_DIR = Path(__name__).resolve().parent

LOG_FILE_NAME = "app_2.log"

LOG_FILE_PATH = BASE_DIR / LOG_FILE_NAME

ERROR_MESSAGES = {
    1: "Battery device error",
    2: "Temperature device error",
    3: "Threshold central error",
}

# captures groups:
#   1: HANDLER
#   2: ID
#   3: S_P_1
#   4: S_P_2
#   5: STATE
LOG_PATTERN = (
    r"'"
      r"(BIG);" # HANDLER
      r"-?[0-9]+;"
      r"([0-9a-zA-Z]{6});" # ID
      r"(?:[0-9]+;){3}"
      r"(-?[0-9]{4});" # S_P_1
      r"(?:-?[0-9]+;){6}"
      r"(-?[0-9]{3});" # S_P_2
      r"(?:-?[0-9]+;){3}"
      r"(02|DD);" # STATE
    r"'")


def get_big_handler_success_count_by_device_id() -> dict:
    """"""
    ...


def parse_message(line: str) -> dict:
    """"Excract HANDLER, ID, S_P_1, S_P_2 and STATE form log line"""
    ...


def inspect_error_message(id, s_p_1, s_p_2):
    """Process messages with STATUS=DD and figure out error messages"""
    ...


def main(filepath: str | Path = LOG_FILE_PATH):
    """Orchestrate the rest of the functions"""
    with open(filepath, "r") as log_file:
        ...


if __name__ == "__main__":
    main()
