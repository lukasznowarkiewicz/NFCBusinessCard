# view.py
import tkinter as tk

class CardView:
    def __init__(self, root):
        self.root = root
        self.root.title("Programowanie Kart Dostępu")

        self.user_id_label = tk.Label(root, text="User ID:")
        self.user_id_label.pack()

        self.user_id_entry = tk.Entry(root)
        self.user_id_entry.pack()

        self.write_button = tk.Button(root, text="Zapisz na karcie", command=lambda: self.on_write())
        self.write_button.pack()

        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

    def on_write(self):
        if self.write_callback:
            self.write_callback(self.user_id_entry.get())

    def set_write_callback(self, callback):
        self.write_callback = callback

    def update_status(self, status):
        self.status_label.config(text=status)
