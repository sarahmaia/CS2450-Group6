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

            #Read, Write and Load instructions (Alan)
            if opcode == 10: 
                self.read(operand)
            elif opcode == 11: 
                self.write(operand)
            elif opcode == 20: 
                 self.load(operand)

            #Store, Add and Subtract instructions (Jalal)
            if opcode == 21: 
                self.store(operand)
            elif opcode == 30: 
                self.add(operand)
            elif opcode == 31: 
                 self.subtract(operand)
                
            if opcode == 40:
                self.branch(operand)
            elif opcode == 41:
                self.branchneg(operand)
            elif opcode == 42:
                self.branchzero(operand)
            
            # POINTER SHOULD BE INCREASED HERE I THINK
            self.instruction_pointer += 1
        
    #Methods for Read, Write, and Load
    def read(self, address):
        self.memory[address] = int(input("Enter a number: "))

    def write(self, address):
        print(self.memory.get(address,0))

    def load(self, address): 
        self.accumulator = self.memory.get(address,0)
        
    #Methods for Store, Add, and Subtract (Jalal)
    def store(self, address):
        self.memory[address] = self.accumulator

    def add(self, address):
        self.accumulator += self.memory.get(address,0)

    def subtract(self, address):
        self.accumulator -= self.memory.get(address,0)
        
    # Divide, multiply, and branch (Sarah)
    def divide(self, address):
        self.accumulator *= self.memory.get(address,0)

    def multiply(self, address):
        self.accumulator /= self.memory.get(address, 0)

    def branch(self, address): 
        self.instruction_pointer = address - 1

    def branchzero(self, address):
        if self.accumulator == 0:
            self.instruction_pointer = address - 1

    def branchneg(self, address):
        if self.accumulator < 0:
            self.instruction_pointer = address - 1

    def halt(self):
        print("Program Halted.")

    
