import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from ..uvsim import UVSim, UVSim_new

import re

class UVSimTab:
    def __init__(self, master, primary_color, secondary_color, use_new_format=False):
        self.master = master
        self.uvsim = UVSim_new() if use_new_format else UVSim()
        self.running = False
        self.primary_color = primary_color
        self.secondary_color = secondary_color

        self.frame = tk.Frame(master, bg=self.primary_color)

        self.accumulator_label = tk.Label(self.frame, text="Accumulator: 0", font=("Arial", 12), bg=self.primary_color)
        self.accumulator_label.pack()

        self.output_display = tk.Label(self.frame, text="Output: ", font=("Arial", 12), bg=self.primary_color)
        self.output_display.pack()

        self.memory_display = tk.Text(self.frame, height=30, width=60, font=("Arial", 12), undo=True, bg=self.secondary_color)
        self.memory_display.pack(pady=10)

        self.button_frame = tk.Frame(self.frame, pady=10, bg=self.primary_color)
        self.button_frame.pack()

        self.load_button = tk.Button(self.button_frame, text="Load Program", width=12, command=self.load_program, bg=self.secondary_color)
        self.save_button = tk.Button(self.button_frame, text="Save Program", width=12, command=self.save_program, bg=self.secondary_color)
        self.run_button = tk.Button(self.button_frame, text="Run", width=12, command=self.run_program, bg=self.secondary_color)
        self.halt_button = tk.Button(self.button_frame, text="Halt", width=12, command=self.halt_program, bg=self.secondary_color)
        self.reset_button = tk.Button(self.button_frame, text="Reset", width=12, command=self.reset_program, bg=self.secondary_color)

        self.load_button.grid(row=0, column=0, padx=5, pady=5)
        self.save_button.grid(row=0, column=1, padx=5, pady=5)
        self.run_button.grid(row=0, column=2, padx=5, pady=5)
        self.halt_button.grid(row=0, column=3, padx=5, pady=5)
        self.reset_button.grid(row=0, column=4, padx=5, pady=5)
        self.check_button = tk.Button(self.button_frame, text="Check Syntax", width=12, command=self.check_syntax, bg=self.secondary_color)
        self.check_button.grid(row=1, column=2, padx=5, pady=5)


    def load_program(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                lines = file.readlines()

            if len(lines) > 250:
                messagebox.showwarning("Warning", "File contains more than 250 lines.\nOnly the first 250 lines will be loaded.")

            self.memory_display.delete("1.0", tk.END)

            for index, line in enumerate(lines):
                if index >= 250:
                    break

                instruction = line.strip().replace(" ", "")
                if instruction == "":
                    continue
                if instruction == "-99999":
                    break

                expected_digits = 6 if isinstance(self.uvsim, UVSim_new) else 4
                if not re.fullmatch(rf"[+-]?\d{{{expected_digits}}}", instruction):
                    messagebox.showerror("Error", f"Expected {expected_digits}-digit instruction at line {index + 1}: '{instruction}'")
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
                        if not all(char in '01' for char in binary_line):
                            messagebox.showerror("Error", f"Invalid binary on line {index + 1}: '{binary_line}'")
                            return
                        file.write(f"{binary_line}\n")
                    file.write("-99999\n")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def run_program(self):
        self.running = True

        # Reset UVSim, keeping the same class (UVSim or UVSim_new)
        self.uvsim = type(self.uvsim)()

        content = self.memory_display.get("1.0", tk.END).strip().splitlines()
        self.uvsim.memory = {}

        for index, line in enumerate(content):
            if line.strip():
                try:
                    self.uvsim.memory[index] = int(line.strip(), 2)
                except ValueError:
                    messagebox.showerror("Error", f"Invalid binary value on line {index + 1}: '{line.strip()}'")
                    self.running = False
                    return

        self.execute_next_instruction()

    def execute_next_instruction(self):
        if not self.running:
            return

        try:
            result = self.uvsim.execute()
        except ValueError as e:
            messagebox.showerror("Execution Error", str(e))
            self.running = False
            return

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
        if self.running:
            self.master.after(250, self.execute_next_instruction)

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
  
    def update_gui(self):
        self.memory_display.delete("1.0", tk.END)
        for val in self.uvsim.memory.values():
            binary_val = format(val if val >= 0 else (1 << 16) + val, '016b')
            self.memory_display.insert(tk.END, f"{binary_val}\n")
        self.accumulator_label.config(text=f"Accumulator: {format(self.uvsim.accumulator if self.uvsim.accumulator >= 0 else (1 << 16) + self.uvsim.accumulator, '016b')}")

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

    def update_colors(self, primary, secondary):
        self.primary_color = primary
        self.secondary_color = secondary
        self.frame.config(bg=primary)
        self.accumulator_label.config(bg=primary)
        self.output_display.config(bg=primary)
        self.memory_display.config(bg=secondary)
        self.button_frame.config(bg=primary)
        for widget in self.button_frame.winfo_children():
            widget.config(bg=secondary)

    def setup_context_menu(self):
        self.context_menu = tk.Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="Cut", command=lambda: self.memory_display.event_generate("<<Cut>>"))
        self.context_menu.add_command(label="Copy", command=lambda: self.memory_display.event_generate("<<Copy>>"))
        self.context_menu.add_command(label="Paste", command=self.safe_paste)

        self.memory_display.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def check_syntax(self):
        self.memory_display.tag_remove("error", "1.0", tk.END)
        self.memory_display.tag_config("error", background="red")

        lines = self.memory_display.get("1.0", tk.END).strip().splitlines()
        errors = []

        for idx, line in enumerate(lines):
            line_clean = line.strip()
            is_valid = False

            if line_clean:
                if line_clean.lstrip("+-").isdigit() and len(line_clean) in [4, 6]:
                    is_valid = True
                elif all(c in "01" for c in line_clean) and len(line_clean) == 16:
                    is_valid = True

            if not is_valid:
                line_start = f"{idx+1}.0"
                line_end = f"{idx+1}.end"
                self.memory_display.tag_add("error", line_start, line_end)
                errors.append(idx + 1)

        if errors:
            messagebox.showerror("Syntax Error", f"Invalid instructions found on lines: {', '.join(map(str, errors))}")
        else:
            messagebox.showinfo("Syntax Check", "No syntax errors found.")



    def safe_paste(self):
        content = self.memory_display.get("1.0", tk.END).strip().splitlines()
        if len(content) >= 250:
            messagebox.showerror("Error", "Cannot paste: Memory size cannot exceed 250 lines.")
            return
        self.memory_display.event_generate("<<Paste>>")
