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
        ndef_message = self.prepare_ndef_message(url)
        r = readers()
        if not r:
            self.notify("Żaden czytnik nie jest dostępny.")
            return

        reader = r[0]
        connection = reader.createConnection()
        try:
            connection.connect()
            
            # Rozpoczęcie zapisu na 4. stronie
            page = 4
            # Wysyłanie komend w blokach po 4 bajty
            while ndef_message:
                block = ndef_message[:4]  # Pobieranie bloku 4 bajtów
                command = [0xFF, 0xD6, 0x00, page, len(block)] + block
                response, sw1, sw2 = connection.transmit(command)
                self.notify_callbacks(f"Wysyłam komendę zapisu na stronę {page}: " + toHexString(command))
                self.notify_callbacks(f"Odpowiedź z karty: SW1={sw1:02X}, SW2={sw2:02X}")
                if sw1 != 0x90 or sw2 != 0x00:
                    self.notify_callbacks(f"Błąd zapisu na stronie {page}.")
                    break
                page += 1
                ndef_message = ndef_message[4:]  # Usuwanie wysłanego bloku

        except NoCardException:
            self.notify("Brak karty w czytniku.")

    def prepare_ndef_message(self, url):
        # Dla prostoty zakładamy, że URL jest już odpowiednio przygotowany i zaczyna się od http://example.com
        # NDEF message dla URLa (http://example.com)
        # 0x03: NDEF Message Begin Mark
        # 0x10: Długość całego rekordu NDEF
        # 0xD1: NDEF Header, MB=1, ME=1, CF=0, SR=1, IL=0, TNF=1
        # 0x01: Typ długości (1 bajt)
        # 0x0C: Długość payload'u (12 bajtów)
        # 0x55: Typ rekordu 'U' (URI)
        # 0x01: Identyfikator URI (0x01 oznacza "http://www.")
        # URL 'example.com' minus 'http://www.' co daje 'example.com'
        # 0xFE: NDEF Message End Mark

        uri_field = url[19:].encode('utf-8')  # Usuwamy 'http://www.' z URL
        payload_length = len(uri_field) + 1  # Długość URL + 1 bajt dla prefixu URI
        header = [0xD1, 0x01, payload_length, 0x55, 0x01]  # Nagłówek NDEF
        full_message = [0x03, payload_length + 5] + header + list(uri_field) + [0xFE]

        return full_message

        
    def notify_callbacks(self, message):
        for callback in self.callbacks:
            callback(message + "\n")


