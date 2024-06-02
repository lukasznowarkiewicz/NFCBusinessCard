# controller.py
import tkinter as tk
import re
class CardController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.view.set_controller(self)
        self.model.register_callback(self.update_view_log)
        self.view.set_write_callback(self.write_card)

    def connectToReader(self):
        self.model.connectToReader()
        self.view.log_text.insert(tk.END, "Próbuje połaczyć się z czytnikiem...")

    def connectToCard(self):
        self.model.connectToCard()


    def clear_card(self):
        self.model.clear_card()
        self.view.log_text.insert(tk.END, "Wysłano rządanie wyczyszczenia do modelu\n")
    
        

    def write_card(self, user_id):
        # W tym miejscu możemy dodać dodatkową walidację lub przetwarzanie danych
        self.model.write_card(user_id)
        self.view.update_status("Dane zostały zapisane na karcie")

    def update_view_log(self, message):
        self.view.log_text.insert(tk.END, message)

    def validate_and_send_command(self, command):
        # Usuwamy wszystkie zbędne znaki oraz zamieniamy popularne separatory na spacje
        command = re.sub(r'[^0-9A-Fa-f]', '', command)
        
        # Dzielenie ciągu na pary znaków (każda para to jeden bajt w hex)
        hex_values = re.findall('.{1,2}', command)  # znajduje wszystkie pary znaków

        # Walidacja, czy wszystkie pary to wartości hex (po usunięciu zbędnych znaków)
        if all(re.fullmatch(r'[0-9A-Fa-f]{2}', value) for value in hex_values):
            apdu = [int(value, 16) for value in hex_values]
            formatted_command = ' '.join(hex_values).upper()
            self.view.update_log(f"Wysyłam komendę: {formatted_command}")
            self.model.send_apdu_command(apdu)
        else:
            self.view.update_log("Błąd: Wprowadzona komenda zawiera niepoprawne wartości szesnastkowe.")

    def save_data(self, text, phone, url):
        errors = []
        if not self.validate_text(text):
            errors.append("Tekst jest pusty lub zawiera nieprawidłowe znaki.")
        if not self.validate_phone(phone):
            errors.append("Numer telefonu jest nieprawidłowy. Powinien zaczynać się od +48 i zawierać 9 kolejnych cyfr.")
        if not self.validate_url(url):
            errors.append("Adres URL jest nieprawidłowy. Powinien zaczynać się od http:// lub https:// i zawierać nazwę domeny.")

        if errors:
            error_message = "Błąd walidacji: " + "; ".join(errors)
            self.view.update_log(error_message)
        else:
            self.view.update_log("Dane zweryfikowane, przesyłam do modelu...")
            self.model.save_ndef_data(text, phone, url)

    def validate_text(self, text):
        # Weryfikacja czy tekst nie jest pusty
        return bool(text.strip())

    def validate_phone(self, phone):
        # Prosta walidacja numeru telefonu (polski format)
        return bool(re.match(r'^\+?48\d{9}$', phone))

    def validate_url(self, url):
        # Walidacja URL za pomocą prostej reguły wyrażeń regularnych
        return bool(re.match(r'^https?:\/\/\S+\.\S+$', url))
