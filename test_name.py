from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from scanner_handler import CheckQr


@pytest.fixture
def check_qr() -> CheckQr:
    return CheckQr()


@pytest.fixture
def check_in_db_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(CheckQr, "check_in_db", return_value=None)


@pytest.fixture
def send_error_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(CheckQr, "send_error")


@pytest.fixture
def can_add_device_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(CheckQr, "can_add_device")


@pytest.mark.parametrize(
    "qr,expected_color,expected_db_error",
    [
        ("123", "Red", "Not in DB"),
        ("12345", "Green", "Not in DB"),
        ("1234567", "Fuzzy Wuzzy", "Not in DB"),
    ],
)
def test_qr_with_correct_len_not_present_in_db(
    check_in_db_mock: MagicMock,
    send_error_mock: MagicMock,
    can_add_device_mock: MagicMock,
    check_qr: CheckQr,
    qr: str,
    expected_color: str,
    expected_db_error: str,
) -> None:
    check_qr.check_scanned_device(qr)

    assert check_qr.color is not None
    assert check_qr.color == expected_color

    send_error_mock.assert_called_once_with(expected_db_error)
    can_add_device_mock.assert_not_called()


@pytest.mark.parametrize(
    "qr,expected_color,expected_message",
    [
        ("123", "Red", "hallelujah 123"),
        ("12345", "Green", "hallelujah 12345"),
        ("1234567", "Fuzzy Wuzzy", "hallelujah 1234567"),
    ],
)
def test_qr_with_correct_len_present_in_db(
    check_in_db_mock: MagicMock,
    send_error_mock: MagicMock,
    can_add_device_mock: MagicMock,
    check_qr: CheckQr,
    qr: str,
    expected_color: str,
    expected_message: str,
) -> None:
    check_in_db_mock.return_value = True

    check_qr.check_scanned_device(qr)

    assert check_qr.color is not None
    assert check_qr.color == expected_color

    send_error_mock.assert_not_called()
    can_add_device_mock.assert_called_once_with(expected_message)


@pytest.mark.parametrize(
    "qr,expected_len_error",
    [
        ("1234", "Error: Wrong qr length 4"),
        ("123456", "Error: Wrong qr length 6"),
        ("12345678", "Error: Wrong qr length 8"),
    ],
)
def test_qr_with_wrong_len_not_present_in_db(
    check_in_db_mock: MagicMock,
    send_error_mock: MagicMock,
    can_add_device_mock: MagicMock,
    check_qr: CheckQr,
    qr: str,
    expected_len_error: str,
) -> None:
    check_qr.check_scanned_device(qr)

    assert check_qr.color is None

    send_error_mock.assert_called_once_with(expected_len_error)

    can_add_device_mock.assert_not_called()


@pytest.mark.parametrize(
    "qr, expected_len_error",
    [
        ("1234", "Error: Wrong qr length 4"),
        ("123456", "Error: Wrong qr length 6"),
        ("12345678", "Error: Wrong qr length 8"),
    ],
)
def test_qr_with_wrong_len_present_in_db(
    check_in_db_mock: MagicMock,
    send_error_mock: MagicMock,
    can_add_device_mock: MagicMock,
    check_qr: CheckQr,
    qr: str,
    expected_len_error: str,
) -> None:
    check_in_db_mock.return_value = True

    check_qr.check_scanned_device(qr)

    assert check_qr.color is None

    send_error_mock.assert_called_once_with(expected_len_error)

    can_add_device_mock.assert_not_called()
