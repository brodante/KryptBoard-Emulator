# app.py
# This is the main entry point for the KryptBoard emulator.

import tkinter as tk
from ui import KryptBoardGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = KryptBoardGUI(root)
    root.mainloop()
