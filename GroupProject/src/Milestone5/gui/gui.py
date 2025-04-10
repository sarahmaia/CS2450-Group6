import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
from ..uvsim import UVSim, UVSim_new
from ..config import load_color_scheme, save_color_scheme, get_format_type
import json


class UVSimGUI:
    def __init__(self, master):
        self.master = master
        master.title("UVSim - BasicML Simulator")
        master.geometry("900x600")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.primary_color, self.secondary_color = load_color_scheme()

        self.uvsim = UVSim()
        self.running = False

        self.top_frame = tk.Frame(master, pady=10)
        self.top_frame.pack()

        self.load_button = tk.Button(self.top_frame, text="Load Program", command=self.load_program)
        self.load_button.pack()

        self.save_button = tk.Button(self.top_frame, text="Save Program", command=self.save_program)
        self.save_button.pack()

        self.change_colors_button = tk.Button(self.top_frame, text="Change Colors", command=self.change_colors)
        self.change_colors_button.pack(pady=5)

        self.memory_frame = tk.Frame(master, padx=10, pady=10, bg=self.primary_color)
        self.memory_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.memory_scroll = tk.Scrollbar(self.memory_frame)
        self.memory_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.memory_display = tk.Text(self.memory_frame, height=30, width=40, yscrollcommand=self.memory_scroll.set, font=("Arial", 12), undo=True)
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

        self.setup_context_menu()

    def setup_context_menu(self):
        self.context_menu = tk.Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="Cut", command=lambda: self.memory_display.event_generate("<<Cut>>"))
        self.context_menu.add_command(label="Copy", command=lambda: self.memory_display.event_generate("<<Copy>>"))
        self.context_menu.add_command(label="Paste", command=self.safe_paste)

        self.memory_display.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def safe_paste(self):
        content = self.memory_display.get("1.0", tk.END).strip().splitlines()
        if len(content) >= 250:
            messagebox.showerror("Error", "Cannot paste: Memory size cannot exceed 250 lines.")
            return
        self.memory_display.event_generate("<<Paste>>")

    def change_colors(self):
        color = colorchooser.askcolor(title="Choose Primary Color")[1]
        if color:
            self.primary_color = color
        color = colorchooser.askcolor(title="Choose Secondary Color")[1]
        if color:
            self.secondary_color = color
        self.update_gui_colors()
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

    def load_program(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                lines = file.readlines()

            self.memory_display.delete("1.0", tk.END)
            
            page_format = get_format_type(lines)
            if page_format == "Invalid instruction":
                messagebox.showerror("Error Invalid instruction")
                return
            if page_format == "new":
                self.uvsim = UVSim_new()
            else:
                self.uvsim = UVSim()

            for index, line in enumerate(lines):
                if index >= 250:
                    break
                instruction = line.strip()
                if instruction == "-99999":
                    break
                if not instruction.lstrip('+-').isdigit():
                    messagebox.showerror("Error", f"Invalid instruction at line {index + 1}: '{instruction}'")
                    return

                value = int(instruction)
                self.uvsim.memory[index] = value
                binary_val = format(value if value >= 0 else (1 << 16) + value, '016b')
                self.memory_display.insert(tk.END, f"{binary_val}\n")


    def save_program(self):
        content = self.memory_display.get("1.0", tk.END).strip().splitlines()
        
        if len(content) > 250:
            messagebox.showerror("Error", "Cannot save: More than 250 lines present.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    for index, line in enumerate(content):
                        binary_line = line.strip()
                        # Validate it's a binary number
                        if not all(char in '01' for char in binary_line):
                            messagebox.showerror("Error", f"Invalid binary on line {index + 1}: '{binary_line}'")
                            return
                        file.write(f"{binary_line}\n")
                    file.write("-99999\n")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")


    def run_program(self):
        self.running = True
        self.uvsim = type(self.uvsim)()
        content = self.memory_display.get("1.0", tk.END).strip().splitlines()
        self.uvsim.memory = {}
        for index, line in enumerate(content):
            if line.strip():
                self.uvsim.memory[index] = int(line.strip(), 2)
        # Execute next instruction after the for loop
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
            self.master.after(250, self.execute_next_instruction)

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
                self.master.after(250, self.execute_next_instruction)
                break
            else:
                messagebox.showerror("Error", "Invalid input. Enter an integer.")

    def update_gui(self):
        self.memory_display.delete("1.0", tk.END)
        for val in self.uvsim.memory.values():
            binary_val = format(val if val >= 0 else (1 << 16) + val, '016b')
            self.memory_display.insert(tk.END, f"{binary_val}\n")
        self.accumulator_label.config(text=f"Accumulator: {format(self.uvsim.accumulator if self.uvsim.accumulator >= 0 else (1 << 16) + self.uvsim.accumulator, '016b')}")

    def halt_program(self):
        self.running = False
        messagebox.showinfo("Info", "Program Halted.")

    def reset_program(self):
        self.running = False
        self.uvsim = type(self.uvsim)()
        self.memory_display.delete("1.0", tk.END)
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
