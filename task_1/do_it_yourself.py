from pathlib import Path


BASE_DIR = Path(__name__).resolve().parent

LOG_FILE_NAME = "app_2.log"

LOG_FILE_PATH = BASE_DIR / LOG_FILE_NAME

ERROR_MESSAGES = {
    1: "Battery device error",
    2: "Temperature device error",
    3: "Threshold central error",
}


def get_big_handler_success_count_by_device_id() -> dict:
    """"""
    ...


def parse_message(line: str) -> dict:
    """"Excract HANDLER, ID, S_P_1, S_P_2 and STATE form log line"""
    ...


def inspect_error_message(id, s_p_1, s_p_2):
    """Process messages with STATUS=DD and figure out error messages"""
    ...


if __name__ == "__main__":
    ...
