import customtkinter as ctk
from gui import AppNatacao

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    app = AppNatacao()
    app.mainloop()
