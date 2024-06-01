# controller.py
class CardController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.view.set_write_callback(self.write_card)

    def write_card(self, user_id):
        # W tym miejscu możemy dodać dodatkową walidację lub przetwarzanie danych
        self.model.write_card(user_id)
        self.view.update_status("Dane zostały zapisane na karcie")
