import unittest
from best_charge import BestCharge


class BestChargeTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_no_promotion(self):
        print("test_no_promotion()")
        tokens = ["ITEM0013 x 4"]
        charge = BestCharge(tokens)
        assert charge.best_charge() == 24

    def test_reward_promotion(self):
        print("test_reward_promotion")
        tokens = ["ITEM0013 x 4", "ITEM0022 x 1"]
        charge = BestCharge(tokens)
        assert charge.best_charge() == 26

    def test_discount_promotion(self):
        print("test_discount_promotion()")
        tokens = ["ITEM0001 x 1", "ITEM0013 x 2", "ITEM0022 x 1"]
        charge = BestCharge(tokens)
        assert charge.best_charge() == 25


if __name__ == '__main__':
    unittest.main()
