from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from fakes import FakeDB
from scanner_handler import CheckQr


@pytest.fixture
def db_fake() -> FakeDB:
    return FakeDB()


@pytest.fixture
def check_qr() -> CheckQr:
    return CheckQr()


@pytest.fixture
def check_in_db_mock(mocker: MockerFixture, db_fake: FakeDB) -> MagicMock:
    return mocker.patch.object(CheckQr, "check_in_db", wraps=db_fake.is_qr_in_db)


@pytest.fixture
def send_error_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(CheckQr, "send_error")


@pytest.fixture
def can_add_device_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(CheckQr, "can_add_device")
