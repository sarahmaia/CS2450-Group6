from uvsim import UVSim
import os

def main():
    
    file_name = input("Enter the program file (e.g., Test1.txt or Test2.txt): ")
    file_path = os.path.join("Milestone2", "tests", file_name)

    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return
    
    # memory = {}
    uvsim = UVSim()

    
    try:
        uvsim.load_program(file_path)
        uvsim.execute()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
