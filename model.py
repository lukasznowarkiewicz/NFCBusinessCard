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

    
    def save_ndef_data(self, text=None, phone=None, url=None):

        # Używamy tylko URL dla prostego przykładu
        ndef_commands = self.prepare_url_ndef_message(url)
        reader_list = readers()
        if not reader_list:
            self.notify("Żaden czytnik nie jest dostępny.")
            return

        reader = reader_list[0]
        connection = reader.createConnection()
        try:
            connection.connect()
            for command in ndef_commands:
                self.notify_callbacks("Wysyłam komendę: " + toHexString(command))
                response, sw1, sw2 = connection.transmit(command)
                # self.notify_callbacks("Odebrano komendę: " + toHexString(response) + toHexString(sw1) + toHexString(sw2))
                if sw1 != 0x90 or sw2 != 0x00:
                    self.notify_callbacks("Błąd zapisu, Status Word: {:02X} {:02X}".format(sw1, sw2))
                    return
            self.notify_callbacks("Dane NDEF zostały zapisane pomyślnie.")
        except NoCardException:
            self.notify_callbacks("Nie wykryto karty.")
        except Exception as e:
            self.notify_callbacks(f"Wystąpił błąd: {str(e)}")
    

    # def prepare_url_ndef_message(self, url):
    #     # Konwersja URL na bajty
    #     url_bytes = url.encode('utf-8')

    #     commands = []
    #     current_page = 4  # Zaczynamy pisać od strony 4 w pamięci NFC tagu

    #     # Dodajemy nagłówek NDEF
    #     header = [0x03, len(url_bytes) + 5, 0xD1, 0x01, len(url_bytes) + 1, 0x55]  # 0x55 oznacza 'U' z "U"RI

    #     # Cały komunikat NDEF, łącząc nagłówek z kodowanym URL
    #     full_message = header + list(url_bytes) + [0xFE]  # 0xFE to znacznik końca NDEF Message

    #     # Dzielimy komunikat na bloki po 4 bajty i pakujemy do komend APDU
    #     while full_message:
    #         chunk = full_message[:4]
    #         full_message = full_message[4:]
    #         if len(chunk) < 4:
    #             chunk += [0x00] * (4 - len(chunk))  # Dopełnienie zerami, jeśli chunk jest krótszy niż 4 bajty
    #         commands.append([0xFF, 0xD6, 0x00, current_page, 0x04] + chunk)
    #         current_page += 1

    #     return commands

    def prepare_url_ndef_message(self, url):
        # Lista predefiniowanych skrótów URI w formacie NDEF
        uri_prefixes = [
            "", "http://www.", "https://www.", "http://", "https://",
            "tel:", "mailto:", "ftp://anonymous:anonymous@", "ftp://ftp.",
            "ftps://", "sftp://", "smb://", "nfs://", "ftp://", "dav://",
            "news:", "telnet://", "imap:", "rtsp://", "urn:", "pop:", "sip:",
            "sips:", "tftp:", "btspp://", "btl2cap://", "btgoep://", "tcpobex://",
            "irdaobex://", "file://", "urn:epc:id:", "urn:epc:tag:", "urn:epc:pat:",
            "urn:epc:raw:", "urn:epc:", "urn:nfc:"
        ]
        
        # Sprawdzanie, czy URL zaczyna się od któregokolwiek ze skrótów
        prefix_code = 0
        for i, prefix in enumerate(uri_prefixes):
            if url.startswith(prefix):
                prefix_code = i
                url = url[len(prefix):]  # Usunięcie skrótu z URLa
                break
        
        # Konwersja pozostałej części URL na bajty
        url_bytes = url.encode('utf-8')
        
        commands = []
        current_page = 4  # Zaczynamy pisać od strony 4 w pamięci NFC tagu
        
        # Dodajemy nagłówek NDEF
        header = [0x03, len(url_bytes) + 5, 0xD1, 0x01, len(url_bytes) + 1, 0x55, prefix_code]
        
        # Cały komunikat NDEF, łącząc nagłówek z kodowanym URL
        full_message = header + list(url_bytes) + [0xFE]  # 0xFE to znacznik końca NDEF Message
        
        # Dzielimy komunikat na bloki po 4 bajty i pakujemy do komend APDU
        while full_message:
            chunk = full_message[:4]
            full_message = full_message[4:]
            if len(chunk) < 4:
                chunk += [0x00] * (4 - len(chunk))  # Dopełnienie zerami, jeśli chunk jest krótszy niż 4 bajty
            commands.append([0xFF, 0xD6, 0x00, current_page, 0x04] + chunk)
            current_page += 1

        return commands



    def prepare_phone_ndef_message(self, url):
        commands = []
        commands.append([0xFF, 0xD6, 0x00, 0x04, 0x04, 0x03, 0x10, 0xD1, 0x01])
        commands.append([0xFF, 0xD6, 0x00, 0x05, 0x04, 0x0C, 0x55, 0x01, 0x65])
        commands.append([0xFF, 0xD6, 0x00, 0x06, 0x04, 0x78, 0x61, 0x6D, 0x70])
        commands.append([0xFF, 0xD6, 0x00, 0x07, 0x04, 0x6C, 0x65, 0x2E, 0x63])
        commands.append([0xFF, 0xD6, 0x00, 0x08, 0x04, 0x6F, 0x6D, 0xFE, 0x00])
        return commands

    def prepare_text_ndef_message(self, url):
        commands = []
        commands.append([0xFF, 0xD6, 0x00, 0x04, 0x04, 0x03, 0x10, 0xD1, 0x01])
        commands.append([0xFF, 0xD6, 0x00, 0x05, 0x04, 0x0C, 0x55, 0x01, 0x65])
        commands.append([0xFF, 0xD6, 0x00, 0x06, 0x04, 0x78, 0x61, 0x6D, 0x70])
        commands.append([0xFF, 0xD6, 0x00, 0x07, 0x04, 0x6C, 0x65, 0x2E, 0x63])
        commands.append([0xFF, 0xD6, 0x00, 0x08, 0x04, 0x6F, 0x6D, 0xFE, 0x00])
        print(commands)
        print(type(commands))
        print(type(commands[0][0]))
        return commands


        
    def notify_callbacks(self, message):
        for callback in self.callbacks:
            callback(message + "\n")


