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
