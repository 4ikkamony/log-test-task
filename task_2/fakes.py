from typing import Optional, Sequence


class FakeDB:
    """
    Fake QR code database for testing

    This class stores QR codes in an internal set
    """

    def __init__(self, qrs: Optional[Sequence[str]] = None):
        self.qrs: set[str] = set(qrs) if qrs else set()

    def is_qr_in_db(self, qr: str) -> Optional[bool]:
        return True if qr in self.qrs else None

    def add_qr(self, qr: str) -> None:
        self.qrs.add(qr)

    def remove_qr(self, qr: str) -> None:
        self.qrs.remove(qr)

    def clear_db(self) -> None:
        self.qrs = set()
