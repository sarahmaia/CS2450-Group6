from uvsim import UVSim

def main():
    file_path = input("Enter the file path: ")
    
    memory = {}
    myfile = UVSim(memory)
    
    myfile.load_program(file_path) 
    myfile.execute()

if __name__ == "__main__":
    main()
