# model.py
from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.Exceptions import NoCardException
import smartcard
import tkinter as tk

class CardModel:
    def __init__(self):
        self.reader = self.detect_reader()
        self.callbacks = []
    
    def register_callback(self, callback):
        self.callbacks.append(callback)

    def detect_reader(self):
        r = readers()
        return r[0] if r else None

    def read_card(self):
        # Logika odczytu danych z karty
        pass

    def write_card(self, data):
        # Logika zapisu danych na karcie
        pass

    def connectToReader(self):
        # Znalezienie wszystkich dostępnych czytników
        card_readers = readers()
        if not card_readers:
            self.notify_callbacks("Nie znaleziono zadnych czytników.")
            return
        self.notify_callbacks("Znaleziono czytniki: " + str(card_readers))

        #Wybranie pierwszego dostępnego
        reader = card_readers[0]
        self.notify_callbacks("Uzywam czytnika: " + str(reader))

    def connectToCard(self):
        # Pobranie listy dostępnych czytników
        r = readers()
        if not r:
            self.log("Żaden czytnik nie jest dostępny.")
            return None

        # Wybór pierwszego dostępnego czytnika
        reader = r[0]
        self.notify_callbacks(f"Używany czytnik: {reader}")

        try:
            # Połączenie z kartą
            connection = reader.createConnection()
            connection.connect()
            atr = connection.getATR()
            self.notify_callbacks(f"ATR karty: {toHexString(atr)}")
            return connection
        except NoCardException:
            self.notify_callbacks("Brak karty w czytniku.")
        except Exception as e:
            self.notify_callbacks(f"Błąd przy nawiązywaniu połączenia: {e}")


        
    def notify_callbacks(self, message):
        for callback in self.callbacks:
            callback(message + "\n")


