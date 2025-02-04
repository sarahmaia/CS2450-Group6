class UVSim:
    def __init__(self, memory: dict):
        self.accumulator = 0  
        self.memory = memory 
        self.instruction_pointer = 0 


    def load_program(self, text_file):
        try:
            with open(text_file, 'r') as file:
                for index, line in enumerate(file):
                    self.memory[index] = int(line.strip())
        except FileNotFoundError:
            print("Error: File not found.")
        except ValueError:
            print("Error: Invalid instruction format.")


    def execute(self):

        while self.instruction_pointer < len(self.memory):
            instruction = self.memory[self.instruction_pointer]
            opcode = instruction // 100
            operand = instruction % 100

            if opcode == 40:
                self.branch(operand)
            elif opcode == 41:
                self.branchneg(operand)
            elif opcode == 42:
                self.branchzero(operand)
            
            # POINTER SHOULD BE INCREASED HERE I THINK


    def branchzero(self, address):
        if self.accumulator == 0:
            self.instruction_pointer = address - 1


    def branchneg(self, address):
        if self.accumulator < 0:
            self.instruction_pointer = address - 1

    

    def halt(self):
        print("Program Halted.")

    