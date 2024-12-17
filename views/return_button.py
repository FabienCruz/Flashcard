import tkinter as tk
from tkinter import ttk

class ReturnButton:
    def __init__(self, screen, manage_screen):
        self.screen = screen
        self.manage_screen = manage_screen

    def initialize_return_button(self):
        self.btn_return = ttk.Button(master=self.screen.frm_bottom, text='Retour', command=self.back_to_game, width=22)
        self.btn_return.pack(side=tk.TOP, padx=5, pady=5)

    def back_to_game(self):
        self.screen.clear_all_frames()
        self.manage_screen.show_game_screen()
