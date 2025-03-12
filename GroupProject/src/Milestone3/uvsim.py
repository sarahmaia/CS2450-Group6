class UVSim:
    def __init__(self):
        self.accumulator = 0  
        self.memory = {}  
        self.instruction_pointer = 0  

    def load_program(self, file_path):
        try:
            with open(file_path, 'r') as file:
                for index, line in enumerate(file):
                    instruction = line.strip()
                    if instruction == "-99999":
                        break
                    self.memory[index] = int(instruction)
        except FileNotFoundError:
            raise FileNotFoundError("File not found.")
        except ValueError:
            raise ValueError("Invalid instruction format.")

    def execute(self):
        while self.instruction_pointer < len(self.memory):
            instruction = self.memory[self.instruction_pointer]
            opcode = instruction // 100
            operand = instruction % 100

            if opcode == 10:  
                return ("read", operand)
            elif opcode == 11:  
                return ("write", operand)
            elif opcode == 20:
                self.load(operand)
            elif opcode == 21:
                self.store(operand)
            elif opcode == 30:
                self.add(operand)
            elif opcode == 31:
                self.subtract(operand)
            elif opcode == 32:
                self.divide(operand)
            elif opcode == 33:
                self.multiply(operand)
            elif opcode == 40:
                self.branch(operand)
            elif opcode == 41:
                self.branchneg(operand)
            elif opcode == 42:
                self.branchzero(operand)
            elif opcode == 43:
                return ("halt", None)  # Stop execution

            self.instruction_pointer += 1

        return None  

    def read_input(self, address, value):
        self.memory[address] = int(value)

    def write_output(self, address):
        return self.memory.get(address, 0)

    def load(self, address):
        if address not in self.memory:
            raise KeyError(f"Error: Address {address} not found in memory")
        self.accumulator = self.memory[address]

    def store(self, address):
        self.memory[address] = self.accumulator

    def add(self, address):
        if address not in self.memory:
            raise KeyError(f"Error: Address {address} not found in memory")
        self.accumulator += self.memory[address]

    def subtract(self, address):
        if address not in self.memory:
            raise KeyError(f"Error: Address {address} not found in memory") 
        self.accumulator -= self.memory[address]

    def divide(self, address):
        if address not in self.memory:
            raise KeyError("Error: Address not found in memory")
        if self.memory[address] == 0:
            print("Error: Division by zero.")
            raise SystemExit
        self.accumulator //= self.memory[address]  

    def multiply(self, address):
        if address not in self.memory:
            raise KeyError("Error: Address not found in memory")
        self.accumulator *= self.memory[address]

    def branch(self, address):
        self.instruction_pointer = address - 1

    def branchneg(self, address):
        if self.accumulator < 0:
            self.instruction_pointer = address - 1

    def branchzero(self, address):
        if self.accumulator == 0:
            self.instruction_pointer = address - 1
