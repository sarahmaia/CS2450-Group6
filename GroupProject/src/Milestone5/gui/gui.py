import tkinter as tk
from tkinter import ttk

from .UVSimTab import UVSimTab

from tkinter import filedialog, messagebox, simpledialog, colorchooser
from ..uvsim import UVSim, UVSim_new
from ..config import load_color_scheme, save_color_scheme, get_format_type
import json


class UVSimGUI:
    def __init__(self, master):
        self.master = master
        master.title("UVSim - BasicML Simulator")
        master.geometry("1200x800")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.primary_color, self.secondary_color = load_color_scheme()

        self.tabs = []

        self.top_frame = tk.Frame(master, bg=self.primary_color, pady=10)
        self.top_frame.pack(fill=tk.X)

        self.new_tab_button = tk.Button(self.top_frame, text="New Tab", command=self.add_tab, bg=self.secondary_color)
        self.new_tab_button.pack(side=tk.LEFT, padx=5)

        self.change_colors_button = tk.Button(self.top_frame, text="Change Colors", command=self.change_colors, bg=self.secondary_color)
        self.change_colors_button.pack(side=tk.LEFT, padx=5)

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.add_tab()  
    
    def add_tab(self):
        new_tab = UVSimTab(self.master, self.primary_color, self.secondary_color)
        self.tabs.append(new_tab)
        self.notebook.add(new_tab.frame, text=f"Program {len(self.tabs)}")
        self.notebook.select(len(self.tabs) - 1)

    def change_colors(self):
        primary = colorchooser.askcolor(title="Choose Primary Color")[1]
        if primary:
            self.primary_color = primary
        secondary = colorchooser.askcolor(title="Choose Secondary Color")[1]
        if secondary:
            self.secondary_color = secondary

        for tab in self.tabs:
            tab.update_colors(self.primary_color, self.secondary_color)

        self.top_frame.config(bg=self.primary_color)
        for widget in self.top_frame.winfo_children():
            widget.config(bg=self.secondary_color)

        save_color_scheme(self.primary_color, self.secondary_color)


    def update_gui_colors(self):
        self.memory_frame.config(bg=self.primary_color)
        self.main_frame.config(bg=self.primary_color)
        self.accumulator_label.config(bg=self.primary_color, fg='black')
        self.output_display.config(bg=self.primary_color, fg='black')
        self.button_frame.config(bg=self.primary_color)
        self.run_button.config(bg=self.secondary_color)
        self.halt_button.config(bg=self.secondary_color)
        self.reset_button.config(bg=self.secondary_color)
        self.memory_display.config(bg=self.secondary_color, fg='black')

    def on_closing(self):
        for tab in self.tabs:
            tab.running = False
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    gui = UVSimGUI(root)
    root.mainloop()
