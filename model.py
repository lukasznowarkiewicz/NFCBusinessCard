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

    
    def save_ndef_data(self, url, text=None, phone=None):

        # Używamy tylko URL dla prostego przykładu
        ndef_commands = self.prepare_ndef_message(url)
        reader_list = readers()
        if not reader_list:
            self.notify("Żaden czytnik nie jest dostępny.")
            return

        reader = reader_list[0]
        connection = reader.createConnection()
        try:
            connection.connect()
            for command in ndef_commands:
                response, sw1, sw2 = connection.transmit(command)
                if sw1 != 0x90 or sw2 != 0x00:
                    self.notify_callbacks("Błąd zapisu, Status Word: {:02X} {:02X}".format(sw1, sw2))
                    return
            self.notify_callbacks("Dane NDEF zostały zapisane pomyślnie.")
        except NoCardException:
            self.notify_callbacks("Nie wykryto karty.")
        except Exception as e:
            self.notify_callbacks(f"Wystąpił błąd: {str(e)}")


    def prepare_ndef_message(self, url):
        from urllib.parse import urlparse
        # Prefix dla 'http://www.'
        uri_prefix = 0x01
        # Odcinamy 'http://' dla skrócenia URL
        parsed_url = urlparse(url)
        short_url = parsed_url.netloc + parsed_url.path

        # Budowa payloadu dla URL
        payload = [ord('U'), uri_prefix] + [ord(c) for c in short_url]

        # Długość payloadu
        payload_length = len(payload)

        # Budowanie NDEF Message
        ndef_header = [0xD1, 0x01, payload_length, 0x55]  # D1 (SR, TNF), Type Length, Payload Length, Type 'U'
        ndef_message = [0x03, payload_length] + ndef_header + payload + [0xFE]  # Dodajemy NDEF Message Start, Payload Length i Terminator NDEF

        # Dodaj padding, jeśli potrzebny
        while len(ndef_message) % 4 != 0:
            ndef_message.append(0x00)  # Dodajemy padding do pełnych stron

        # Podziel na strony
        pages = [ndef_message[i:i+4] for i in range(0, len(ndef_message), 4)]
        # Przygotuj komendy zapisu
        commands = []
        for page_number, page in enumerate(pages, start=4):  # Początkowa strona dla danych NDEF to 4
            command = [0xFF, 0xD6, 0x00, page_number, 0x04] + page
            commands.append(command)

        return commands


        
    def notify_callbacks(self, message):
        for callback in self.callbacks:
            callback(message + "\n")


