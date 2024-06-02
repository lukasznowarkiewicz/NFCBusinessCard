# model.py
from smartcard.System import readers
from smartcard.util import toHexString
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

    def clear_card(self):
        # Logika odpowiedzialna za czyszczenie danych karty NFC
        try:
            # Symulacja operacji na karcie, np. poprzez interfejs API czytnika
            # Można tutaj wywołać rzeczywiste funkcje czytnika kart NFC
            print("Próba czyszczenia danych z karty NFC...")
            self.notify_callbacks("Callback z modelu")
            
            # Załóżmy, że interfejs czytnika ma funkcję erase_card()
            # reader.erase_card()

            print("Czyszczenie karty zakończone sukcesem.")
            return "Czyszczenie karty zakończone sukcesem."
        except Exception as e:
            error_msg = f"Błąd przy czyszczeniu karty: {e}"
            print(error_msg)
            return error_msg
        
    def notify_callbacks(self, message):
        for callback in self.callbacks:
            callback(message)

            
