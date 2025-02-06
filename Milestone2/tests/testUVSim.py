import unittest
from Milestone2.uvsim import UVSim

class TestUVSim(unittest.TestCase):
    
    def setUp(self):
        self.memory = {}
        self.uvsim = UVSim(self.memory)
    
    def test_load_accumulator(self):
        self.uvsim.memory[5] = 55
        self.uvsim.load(5)
        self.assertEqual(self.uvsim.accumulator, 55)

    # def test_halt(self):
    #     self.uvsim.halt()
    #     self.assertEqual(self.uvsim.instruction_pointer, -1) 

    def test_branch(self):
        self.uvsim.memory[5] = 10
        self.uvsim.branch(5)
        self.assertEqual(self.uvsim.instruction_pointer, 4)

    def test_branch_zero(self):
        self.uvsim.memory[5] = 0
        self.uvsim.load(5)
        self.uvsim.branchzero(10)
        self.assertEqual(self.uvsim.instruction_pointer, 9)

    def test_branch_neg(self):
        self.uvsim.memory[5] = -1
        self.uvsim.load(5)
        self.uvsim.branchneg(10)
        self.assertEqual(self.uvsim.instruction_pointer, 9)
        


if __name__ == "__main__":
    unittest.main()

# python -m Milestone2.tests.testUVSim