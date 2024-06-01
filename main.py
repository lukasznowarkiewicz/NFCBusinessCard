# main.py
import tkinter as tk
from model import CardModel
from view import CardView
from controller import CardController

def main():
    root = tk.Tk()
    model = CardModel()
    view = CardView(root)
    controller = CardController(view, model)
    root.mainloop()

if __name__ == "__main__":
    main()
