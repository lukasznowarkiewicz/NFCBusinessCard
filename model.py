# model.py
from smartcard.System import readers
from smartcard.util import toHexString

class CardModel:
    def __init__(self):
        self.reader = self.detect_reader()

    def detect_reader(self):
        r = readers()
        return r[0] if r else None

    def read_card(self):
        # Logika odczytu danych z karty
        pass

    def write_card(self, data):
        # Logika zapisu danych na karcie
        pass
