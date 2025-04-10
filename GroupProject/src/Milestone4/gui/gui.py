import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser, ttk
import json
from uvsim import UVSim


#ALAN'S VERSION
class UVSimTab:
    def __init__(self, parent, master, primary_color, secondary_color):
        self.parent = parent
        self.master = master
        self.uvsim = UVSim()
        self.running = False
        self.primary_color = primary_color
        self.secondary_color = secondary_color

        self.frame = tk.Frame(master, bg=self.primary_color)

        self.accumulator_label = tk.Label(self.frame, text="Accumulator: 0", font=("Arial", 12), bg=self.primary_color, fg='black')
        self.accumulator_label.pack()

        self.output_display = tk.Label(self.frame, text="Output: ", font=("Arial", 12), bg=self.primary_color, fg='black')
        self.output_display.pack()

        self.memory_display = tk.Text(self.frame, height=30, width=60, font=("Arial", 12), undo=True, bg=self.secondary_color, fg='black')
        self.memory_display.pack(pady=10)

        self.button_frame = tk.Frame(self.frame, pady=10, bg=self.primary_color)
        self.button_frame.pack()

        self.load_button = tk.Button(self.button_frame, text="Load Program", width=12, command=self.load_program, bg=self.secondary_color, fg="black")
        self.save_button = tk.Button(self.button_frame, text="Save Program", width=12, command=self.save_program, bg=self.secondary_color, fg="black")
        self.run_button = tk.Button(self.button_frame, text="Run", width=12, command=self.run_program, bg=self.secondary_color, fg="black")
        self.halt_button = tk.Button(self.button_frame, text="Halt", width=12, command=self.halt_program, bg=self.secondary_color, fg="black")
        self.reset_button = tk.Button(self.button_frame, text="Reset", width=12, command=self.reset_program, bg=self.secondary_color, fg="black")

        self.load_button.grid(row=0, column=0, padx=5, pady=5)
        self.save_button.grid(row=0, column=1, padx=5, pady=5)
        self.run_button.grid(row=0, column=2, padx=5, pady=5)
        self.halt_button.grid(row=0, column=3, padx=5, pady=5)
        self.reset_button.grid(row=0, column=4, padx=5, pady=5)

    def load_program(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.memory_display.delete("1.0", tk.END)
                self.memory_display.insert(tk.END, content)

    def save_program(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            content = self.memory_display.get("1.0", tk.END).strip()
            with open(file_path, "w") as file:
                file.write(content)

    def run_program(self):
        self.running = True
        self.uvsim = UVSim()
        content = self.memory_display.get("1.0", tk.END).strip().splitlines()
        self.uvsim.memory = {}
        for index, line in enumerate(content):
            if line.strip():
                try:
                    if all(c in '01' for c in line.strip()) and len(line.strip()) == 16:
                        self.uvsim.memory[index] = int(line.strip(), 2)
                    else:
                        self.uvsim.memory[index] = int(line.strip())
                except ValueError:
                    messagebox.showerror("Error", f"Invalid line at {index + 1}: '{line.strip()}'")
                    self.running = False
                    return

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

        self.update_gui()
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
                break
            else:
                messagebox.showerror("Error", "Invalid input. Enter an integer.")

    def update_gui(self):
        self.memory_display.delete("1.0", tk.END)
        for address in sorted(self.uvsim.memory.keys()):
            val = self.uvsim.memory[address]
            binary_val = format(val if val >= 0 else (1 << 16) + val, '016b')
            self.memory_display.insert(tk.END, f"{binary_val}\n")
        self.accumulator_label.config(text=f"Accumulator: {format(self.uvsim.accumulator if self.uvsim.accumulator >= 0 else (1 << 16) + self.uvsim.accumulator, '016b')}")

    def halt_program(self):
        self.running = False
        messagebox.showinfo("Info", "Program Halted.")

    def reset_program(self):
        self.running = False
        self.uvsim = UVSim()
        self.memory_display.delete("1.0", tk.END)
        self.accumulator_label.config(text="Accumulator: 0")
        self.output_display.config(text="Output: ")
        messagebox.showinfo("Info", "Program Reset")

class UVSimGUI:
    def __init__(self, master):
        self.master = master
        master.title("UVSim - BasicML Simulator")
        master.geometry("1920x1080")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.load_color_scheme()

        self.top_frame = tk.Frame(master, pady=10, bg=self.primary_color)
        self.top_frame.pack(fill=tk.X)

        self.new_tab_button = tk.Button(self.top_frame, text="New Tab", command=self.add_tab, bg=self.secondary_color, fg="black")
        self.new_tab_button.pack(side=tk.LEFT, padx=5)

        self.change_colors_button = tk.Button(self.top_frame, text="Change Colors", command=self.change_colors, bg=self.secondary_color, fg="black")
        self.change_colors_button.pack(side=tk.LEFT, padx=5)

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tabs = []
        self.add_tab()

    def load_color_scheme(self):
        try:
            with open("config.json", "r") as file:
                config = json.load(file)
                self.primary_color = config.get("primary_color", "#4C721D")
                self.secondary_color = config.get("secondary_color", "#FFFFFF")
        except FileNotFoundError:
            self.primary_color = "#4C721D"
            self.secondary_color = "#FFFFFF"
            self.save_color_scheme()

    def save_color_scheme(self):
        config = {
            "primary_color": self.primary_color,
            "secondary_color": self.secondary_color
        }
        with open("config.json", "w") as file:
            json.dump(config, file)

    def change_colors(self):
        primary = colorchooser.askcolor(title="Choose Primary Color")[1]
        if primary:
            self.primary_color = primary
        secondary = colorchooser.askcolor(title="Choose Secondary Color")[1]
        if secondary:
            self.secondary_color = secondary
        for tab in self.tabs:
            tab.frame.config(bg=self.primary_color)
            tab.memory_display.config(bg=self.secondary_color)
            tab.accumulator_label.config(bg=self.primary_color)
            tab.output_display.config(bg=self.primary_color)
            tab.button_frame.config(bg=self.primary_color)
            for widget in tab.button_frame.winfo_children():
                widget.config(bg=self.secondary_color, fg="black")
        self.top_frame.config(bg=self.primary_color)
        for widget in self.top_frame.winfo_children():
            widget.config(bg=self.secondary_color, fg="black")
        self.save_color_scheme()

    def add_tab(self):
        tab = UVSimTab(self, self.master, self.primary_color, self.secondary_color)
        self.tabs.append(tab)
        self.notebook.add(tab.frame, text=f"Program {len(self.tabs)}")
        self.notebook.select(len(self.tabs) - 1)

    def on_closing(self):
        for tab in self.tabs:
            tab.running = False
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UVSimGUI(root)
    root.mainloop()
