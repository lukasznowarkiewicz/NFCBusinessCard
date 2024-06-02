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

            # Komenda GET DATA do odczytu UID
            GET_DATA_COMMAND = [0xFF, 0xCA, 0x00, 0x00, 0x00]
            data, sw1, sw2 = connection.transmit(GET_DATA_COMMAND)
            self.notify_callbacks("Wysłane rządzanie UID: " + toHexString(GET_DATA_COMMAND))
            if sw1 == 0x90 and sw2 == 0x00:
                uid = toHexString(data)
                self.notify_callbacks(f"Otrzymane UID karty: {uid}")
                return uid
            else:
                self.notify_callbacks("Nie udało się odczytać UID karty.")
                return None

            return connection
        except NoCardException:
            self.notify_callbacks("Brak karty w czytniku.")
        except Exception as e:
            self.notify_callbacks(f"Błąd przy nawiązywaniu połączenia: {e}")

    def send_apdu_command(self, apdu):
        r = readers()
        if not r:
            self.notify("Żaden czytnik nie jest dostępny.")
            return

        reader = r[0]
        connection = reader.createConnection()
        try:
            connection.connect()
            response, sw1, sw2 = connection.transmit(apdu)
            full_response = toHexString(response + [sw1, sw2])
            self.notify_callbacks(f"Odpowiedź z karty: {full_response}")
        except Exception as e:
            self.notify_callbacks(f"Błąd komunikacji z kartą: {e}")

    
    def save_ndef_data(self, text, phone, url):
        # Składanie danych NDEF
        ndef_message = self.prepare_ndef_message(text, phone, url)
        r = readers()
        if not r:
            self.notify_callbacks("Żaden czytnik nie jest dostępny.")
            return

        reader = r[0]
        connection = reader.createConnection()
        try:
            connection.connect()
            # Przykładowa komenda APDU do zapisu danych NDEF
            # Należy dostosować komendy do specyfiki karty
            command = [0xFF, 0xD6, 0x00, 0x04, len(ndef_message)] + ndef_message
            command_hex = toHexString(command)
            self.notify_callbacks("Wysyłam komendę zapisu: " + toHexString(command))
            response, sw1, sw2 = connection.transmit(command)
            self.notify_callbacks(f"Odpowiedź z karty: SW1={sw1:02X}, SW2={sw2:02X}")
        except NoCardException:
            self.notify_callbacks("Brak karty w czytniku.")
        
    # def prepare_ndef_message(self, text, phone, url):
    #     # Prosta implementacja rekordu URI NDEF
    #     # Dla przykładu, skupimy się na zapisie URL
    #     uri_prefix = b'\x01'  # Prefiks dla "http://www."
    #     uri_field = url.encode('utf-8')
    #     return [0xD1, 0x01, len(uri_field) + 1, 0x55, uri_prefix] + list(uri_field)

    def prepare_ndef_message(self, text, phone, url):
        # Zakładając, że skupiamy się na zapisie URL jako rekordu NDEF
        # 0xD1: MB/ME=1, CF=0, SR=1, IL=0, TNF=1 (NFC Well Known Type)
        # 0x01: Typ długości - 1 bajt
        # Długość ładunku = długość prefixu (1 bajt) + długość URL
        # 0x55: Typ rekordu - 'U' (URI)
        # 0x01: Wartość prefixu dla "http://www."
        
        if not url.startswith("http://www."):
            url = "http://www." + url  # Prosta normalizacja URL
        
        uri_field = url.encode('utf-8')[11:]  # Zakładamy, że "http://www." jest już uwzględnione
        payload_length = len(uri_field) + 1  # Długość URL + 1 bajt prefixu
        header = [0xD1, 0x01, payload_length, 0x55, 0x01]  # Nagłówek NDEF
        full_message = header + list(uri_field)
        
        return full_message

        
    def notify_callbacks(self, message):
        for callback in self.callbacks:
            callback(message + "\n")


