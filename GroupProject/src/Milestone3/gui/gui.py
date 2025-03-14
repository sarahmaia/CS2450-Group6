import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
import json

from src.Milestone3.uvsim import UVSim

class UVSimGUI:
    def __init__(self, master):
        self.master = master
        master.title("UVSim - BasicML Simulator")
        master.geometry("900x600")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Load color scheme
        self.load_color_scheme()

        self.uvsim = UVSim()
        self.running = False  

        self.top_frame = tk.Frame(master, pady=10)
        self.top_frame.pack()

        self.load_button = tk.Button(self.top_frame, text="Load Program", command=self.load_program)
        self.load_button.pack()

        self.memory_frame = tk.Frame(master, padx=10, pady=10, bg=self.primary_color)
        self.memory_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.memory_scroll = tk.Scrollbar(self.memory_frame)
        self.memory_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.memory_display = tk.Text(self.memory_frame, height=30, width=40, yscrollcommand=self.memory_scroll.set, font=("Arial", 12))
        self.memory_display.pack(side=tk.LEFT, fill=tk.Y)

        self.memory_scroll.config(command=self.memory_display.yview)

        self.main_frame = tk.Frame(master, padx=20, pady=10, bg=self.primary_color)
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.accumulator_label = tk.Label(self.main_frame, text="Accumulator: 0", font=("Arial", 12), bg=self.primary_color, fg='black')
        self.accumulator_label.pack()

        self.output_display = tk.Label(self.main_frame, text="Output: ", font=("Arial", 12), bg=self.primary_color, fg='black')
        self.output_display.pack()

        self.button_frame = tk.Frame(self.main_frame, pady=10, bg=self.primary_color)
        self.button_frame.pack()

        self.run_button = tk.Button(self.button_frame, text="Run", width=12, command=self.run_program)
        self.halt_button = tk.Button(self.button_frame, text="Halt", width=12, command=self.halt_program)
        self.reset_button = tk.Button(self.button_frame, text="Reset", width=12, command=self.reset_program)

        self.run_button.grid(row=0, column=0, padx=5, pady=5)
        self.halt_button.grid(row=1, column=0, padx=5, pady=5)
        self.reset_button.grid(row=1, column=1, padx=5, pady=5)

        # Button to change color scheme
        self.change_colors_button = tk.Button(self.top_frame, text="Change Colors", command=self.change_colors)
        self.change_colors_button.pack(pady=5)

    def load_color_scheme(self):
        """Load the color scheme from a configuration file."""
        try:
            with open("config.json", "r") as file:
                config = json.load(file)
                self.primary_color = config.get("primary_color", "#4C721D")  # Default UVU dark green
                self.secondary_color = config.get("secondary_color", "#FFFFFF") 
        except FileNotFoundError:
            # If config file does not exist, default to UVU color scheme
            self.primary_color = "#4C721D"
            self.secondary_color = "#FFFFFF"
            self.save_color_scheme()

    def save_color_scheme(self):
        """Save the current color scheme to a configuration file."""
        config = {
            "primary_color": self.primary_color,
            "secondary_color": self.secondary_color
        }
        with open("config.json", "w") as file:
            json.dump(config, file)

    def change_colors(self):
        """Allow the user to choose a primary and secondary color."""
        color = colorchooser.askcolor(title="Choose Primary Color")[1]
        if color:
            self.primary_color = color
            self.update_gui_colors()

        color = colorchooser.askcolor(title="Choose Secondary Color")[1]
        if color:
            self.secondary_color = color
            self.update_gui_colors()

        # Save the new colors to the configuration file
        self.save_color_scheme()

    def update_gui_colors(self):
        """Update the colors of the GUI elements."""
        self.memory_frame.config(bg=self.primary_color)
        self.main_frame.config(bg=self.primary_color)

        self.accumulator_label.config(bg=self.primary_color, fg='black')
        self.output_display.config(bg=self.primary_color, fg='black')

        self.button_frame.config(bg=self.primary_color)
        self.run_button.config(bg=self.secondary_color)
        self.halt_button.config(bg=self.secondary_color)
        self.reset_button.config(bg=self.secondary_color)

        self.memory_display.config(bg=self.secondary_color, fg='black')

    def load_program(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.memory_display.delete(1.0, tk.END)  
            self.uvsim.load_program(file_path)

            for index, value in self.uvsim.memory.items():
                self.memory_display.insert(tk.END, f"{index:02d}: {value}\n") 

    def run_program(self):
        self.running = True
        self.execute_next_instruction()

    def execute_next_instruction(self):
        if not self.running:
            return
            
        result = self.uvsim.execute()
        if not result:
            self.running = False
            return

        operation, address = result

        if operation == "read":
            self.running = False  
            self.prompt_user_input(address)
            return  

        elif operation == "write":
            output_value = self.uvsim.write_output(address)
            self.output_display.config(text=f"Output: {output_value}")

        elif operation == "halt":
            self.running = False
            messagebox.showinfo("Info", "Program Halted.")
            return

        self.uvsim.instruction_pointer += 1  

        if self.running:
            self.master.after(100, self.execute_next_instruction)

    def prompt_user_input(self, address):
        while True:
            user_input = simpledialog.askstring("Input", f"Enter a number for address {address}:")
            
            if user_input is None: 
                messagebox.showinfo("Info", "Program Halted by User")
                self.running = False
                return
            
            if user_input.lstrip('-').isdigit():  
                self.uvsim.memory[address] = int(user_input) 
                self.uvsim.instruction_pointer += 1  
                self.running = True
                self.update_gui()
                self.master.after(100, self.execute_next_instruction) 
                break  # Exit loop
            else:
                messagebox.showerror("Error", "Invalid input. Enter an integer.")

    def update_gui(self):
        self.memory_display.delete(1.0, tk.END)  
        for index, value in self.uvsim.memory.items():
            self.memory_display.insert(tk.END, f"{index:02d}: {value}\n")

        self.accumulator_label.config(text=f"Accumulator: {self.uvsim.accumulator}")

    def halt_program(self):
        self.running = False
        messagebox.showinfo("Info", "Program Halted.")

    def reset_program(self):
        self.running = False
        self.uvsim = UVSim()  
        self.memory_display.delete(1.0, tk.END)
        self.accumulator_label.config(text="Accumulator: 0")
        self.output_display.config(text="Output: ")
        messagebox.showinfo("Info", "Program Reset")

    def on_closing(self):
        self.running = False
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    gui = UVSimGUI(root)
    root.mainloop()


    # python -m src.Milestone3.gui.gui
    # from src.Milestone3.uvsim import UVSim
