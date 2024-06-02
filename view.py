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
            default_text = tk.StringVar(root, value="Cokolwiek")
            self.text_entry = tk.Entry(root, width=50, textvariable=default_text)
            self.text_entry.pack()

            # Tworzenie Label i Entry dla Numeru Telefonu
            self.phone_label = tk.Label(root, text="Numer telefonu:", bg='gray12', fg='white')
            self.phone_label.pack(pady=(20, 0))
            default_phone = tk.StringVar(root, value="+48601100100")
            self.phone_entry = tk.Entry(root, width=50, textvariable=default_phone)
            self.phone_entry.pack()

            # Tworzenie Label i Entry dla URL
            self.url_label = tk.Label(root, text="Adres URL:", bg='gray12', fg='white')
            self.url_label.pack(pady=(20, 0))
            default_url = tk.StringVar(root, value="http://google.com")
            self.url_entry = tk.Entry(root, width=50, textvariable=default_url)
            self.url_entry.pack()

            # Przyciski do programowania i czyszczenia karty
            self.write_button = tk.Button(root, text="Programuj kartę", command=self.on_save_data, bg='deep sky blue')
            self.write_button.pack(pady=(20, 0))
            self.clear_button = tk.Button(root, text="Czyść kartę", command=self.on_clear, bg='red3')
            self.clear_button.pack()
 
            # Pole tekstowe na komendy APDU
            self.command_entry = tk.Entry(self.root, width=40)
            self.command_entry.pack(pady=10)

            # Przycisk do wysyłania komendy
            self.send_button = tk.Button(self.root, text="Wyślij Komendę", command=self.send_command)
            self.send_button.pack(pady=10)

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

    def send_command(self):
        command = self.command_entry.get()
        self.controller.validate_and_send_command(command)

    def on_save_data(self):
        text_data = self.text_entry.get()
        phone_data = self.phone_entry.get()
        url_data = self.url_entry.get()
        self.controller.save_data(text_data, phone_data, url_data)

    def update_log(self, message):
         self.log_text.insert(tk.END, message + "\n")
