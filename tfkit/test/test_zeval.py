import unittest

import os


class TestEval(unittest.TestCase):

    def testHelp(self):
        result = os.system('tfkit-eval -h')
        self.assertTrue(result == 0)

    def testEvalOnGen(self):
        result = os.system(
            'tfkit-eval --model ./cache/10.pt --valid ../demo_data/generate.csv --metric classification --print')
        self.assertTrue(result == 0)
        result = os.system(
            'tfkit-eval --model ./cache/10.pt --valid ../demo_data/generate.csv --metric emf1 --print --beamsearch --outfile')
        self.assertTrue(result == 0)

    def testEvalClassify(self):
        result = os.system(
            'tfkit-eval --model ./cache/10.pt --valid ../demo_data/classification.csv --metric classification --print  --outfile')
        self.assertTrue(result == 0)
