import unittest

import os

import pytest


class TestTrain(unittest.TestCase):

    def testHelp(self):
        result = os.system('tfkit-train -h')
        assert (result == 0)

    @pytest.mark.skip()
    def testMultiClass(self):
        result = os.system(
            'tfkit-train --batch 2 --epoch 2  --train ../demo_data/classification.csv ../demo_data/generate.csv --lr 5e-5 --valid ../demo_data/classification.csv ../demo_data/generate.csv --model clas onebyone --config voidful/albert_chinese_tiny  --savedir ./cache/ --maxlen 50')
        self.assertTrue(result == 0)

    @pytest.mark.skip()
    def testGenOneByOne(self):
        result = os.system(
            'tfkit-train --batch 2 --epoch 2  --train ../demo_data/generate.csv --valid ../demo_data/generate.csv --model onebyone --config voidful/albert_chinese_tiny  --savedir ./cache/ --maxlen 50')
        self.assertTrue(result == 0)

    @pytest.mark.skip()
    def testGenWithSentLoss(self):
        result = os.system(
            'tfkit-train --batch 2 --epoch 2  --train ../demo_data/generate.csv --valid ../demo_data/generate.csv --model onebyone-pos --config voidful/albert_chinese_tiny  --savedir ./cache/ --maxlen 50')
        self.assertTrue(result == 0)

    @pytest.mark.skip()
    def testClassify(self):
        result = os.system(
            'tfkit-train --lr 1e-4 --grad_accum 2 --batch 2 --epoch 2 --train ../demo_data/classification.csv --valid ../demo_data/classification.csv --model clas --config voidful/albert_chinese_tiny  --savedir ./cache/ --maxlen 50')
        self.assertTrue(result == 0)


