# view.py
import tkinter as tk

class CardView:
    def __init__(self, root):
            self.root = root
            self.root.geometry("800x600")
            self.root.title("Programowanie elektronicznej wizytówki")
            self.root.configure(bg='gray12')
            self.controller = None

            # Tworzenie  Entry dla łączenia z czytnikiem
            self.connect_button = tk.Button(root, text="Połącz z czytnikiem", command=self.on_connect, bg='red3')
            self.connect_button.pack()
            
            # Tworzenie  Entry dla łączenia z kartą
            self.connect_button = tk.Button(root, text="Połącz z kartą", command=self.on_connect_card, bg='red3')
            self.connect_button.pack()

            # Tworzenie Label i Entry dla Tekstu
            self.text_label = tk.Label(root, text="Text:", bg='gray12', fg='white')
            self.text_label.pack(pady=(20, 0))
            self.text_entry = tk.Entry(root, width=50)
            self.text_entry.pack()

            # Tworzenie Label i Entry dla Numeru Telefonu
            self.phone_label = tk.Label(root, text="Numer telefonu:", bg='gray12', fg='white')
            self.phone_label.pack(pady=(20, 0))
            self.phone_entry = tk.Entry(root, width=50)
            self.phone_entry.pack()

            # Tworzenie Label i Entry dla URL
            self.url_label = tk.Label(root, text="Adres URL:", bg='gray12', fg='white')
            self.url_label = tk.Label(root, text="Adres URL:", bg='gray12', fg='white')
            self.url_label.pack(pady=(20, 0))
            self.url_entry = tk.Entry(root, width=50)
            self.url_entry.pack()

            # Przyciski do programowania i czyszczenia karty
            self.write_button = tk.Button(root, text="Programuj kartę", command=self.on_write, bg='deep sky blue')
            self.write_button.pack(pady=(20, 0))
            self.clear_button = tk.Button(root, text="Czyść kartę", command=self.on_clear, bg='red3')
            self.clear_button.pack()

            # Pole tekstowe do wyświetlania logów
            self.log_text = tk.Text(root, height=10, width=80, bg='gray30', fg='white')
            self.log_text.pack(pady=(20, 0))
    def set_controller(self, controller):
         self.controller = controller

    def on_connect(self):
        self.controller.connectToReader()

    def on_connect_card(self):
         self.controller.connectToCard()

    def on_write(self):
        if self.write_callback:
            self.write_callback(self.user_id_entry.get())

    def on_clear(self):
        if self.controller:
            self.controller.clear_card()
        self.log_text.insert(tk.END, "Wyslano rzadanie czyszczenia karty do controllera...\n")

    def set_write_callback(self, callback):
        self.write_callback = callback

    def update_status(self, status):
        self.status_label.config(text=status)
