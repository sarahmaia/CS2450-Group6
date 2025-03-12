import unittest
from unittest.mock import MagicMock
from src.Milestone3.uvsim import UVSim

class TestUVSim(unittest.TestCase):
    
    def setUp(self):
        self.memory = {}
        self.uvsim = UVSim()

    def test_load_valid_program(self):
        self.uvsim.memory[0] = 2005
        self.assertEqual(self.uvsim.memory[0], 2005)

    def test_load_invalid_program(self):
        with self.assertRaises(FileNotFoundError):
            self.uvsim.load_program("invalid_program.txt")

    def test_execute_halt(self):
        self.uvsim.memory[0] = 4300
        result = self.uvsim.execute()
        self.assertEqual(result, ("halt", None))

    # Read input
    def test_read_valid_input(self):
        self.uvsim.read_input(10, 42)
        self.assertEqual(self.uvsim.memory[10], 42)

    def test_read_invalid_input(self):
        with self.assertRaises(ValueError):
            self.uvsim.read_input(10, "abc")


    # Write output
    def test_write_output(self):
        self.uvsim.memory[10] = 99
        output = self.uvsim.write_output(10)
        self.assertEqual(output, 99)

    def test_write_uninitialized_memory(self):
        with unittest.mock.patch("builtins.print") as mock_print:
            self.uvsim.write_output(99)
            mock_print.assert_called_with(0)

    # 05. Load Value
    def test_load_accumulator(self):
        self.uvsim.memory[5] = 55
        self.uvsim.load(5)
        self.assertEqual(self.uvsim.accumulator, 55)

    def test_load_invalid_memory(self):
        with self.assertRaises(KeyError):
            self.uvsim.load(150)

     # 06. Store Value
    def test_store_accumulator(self):
        self.uvsim.accumulator = 77
        self.uvsim.store(3)
        self.assertEqual(self.uvsim.memory[3], 77)

    # 07. Add
    def test_add_value(self):
        self.uvsim.accumulator = 10
        self.uvsim.memory[6] = 15
        self.uvsim.add(6)
        self.assertEqual(self.uvsim.accumulator, 25)

    def test_add_invalid_memory(self):
        with self.assertRaises(KeyError):
            self.uvsim.add(150)

    # 08. Subtract
    def test_subtract_value(self):
        self.uvsim.accumulator = 10
        self.uvsim.memory[2] = 4
        self.uvsim.subtract(2)
        self.assertEqual(self.uvsim.accumulator, 6)

    def test_subtract_invalid_memory(self):
        with self.assertRaises(KeyError):
            self.uvsim.subtract(150)
        
    # 09. Multiply
    def test_multiply_value(self):
        self.uvsim.accumulator = 3
        self.uvsim.memory[1] = 4
        self.uvsim.multiply(1)
        self.assertEqual(self.uvsim.accumulator, 12)

    def test_multiply_by_zero(self):
        self.uvsim.accumulator = 5
        self.uvsim.memory[9] = 0
        self.uvsim.multiply(9)
        self.assertEqual(self.uvsim.accumulator, 0)

        

    # 10. Divide
    def test_divide_valid(self):
        self.uvsim.accumulator = 10
        self.uvsim.memory[3] = 2
        self.uvsim.divide(3)
        self.assertEqual(self.uvsim.accumulator, 5)

    def test_divide_by_zero(self):
        self.uvsim.accumulator = 100
        self.uvsim.memory[4] = 0
        with self.assertRaises(SystemExit):
            self.uvsim.divide(4)

        # DIVIDE BY 0 SHOULD RAISE AN ERROR OR SYSTEM EXIT

    # 11. Branch
    def test_branch(self):
        self.uvsim.branch(5)
        self.assertEqual(self.uvsim.instruction_pointer, 4)

    # 12. Branch if negative
    def test_branchneg_negative(self):
        self.uvsim.accumulator = -5
        self.uvsim.branchneg(10)
        self.assertEqual(self.uvsim.instruction_pointer, 9)

    def test_branchneg_positive(self):
        self.uvsim.accumulator = 5
        self.uvsim.branchneg(10)
        self.assertNotEqual(self.uvsim.instruction_pointer, 9)

    # 13. Branch if zero
    def test_branchzero_zero(self):
        self.uvsim.accumulator = 0
        self.uvsim.branchzero(20)
        self.assertEqual(self.uvsim.instruction_pointer, 19)

    def test_branchzero_nonzero(self):
        self.uvsim.accumulator = 10
        self.uvsim.branchzero(20)
        self.assertNotEqual(self.uvsim.instruction_pointer, 19)

    # 14. Halt
    def test_halt_execution(self):
        result = self.uvsim.execute()
        self.assertEqual(result, None)


if __name__ == "__main__":
    unittest.main()

# python -m Milestone2.tests.testUVSim












