# controller.py
import tkinter as tk
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
        
