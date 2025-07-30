import random
import unittest
from unittest.mock import patch

from faker import Faker

from dming.dice import roll

faker = Faker()


class TestNormalRoll(unittest.TestCase):
    @patch("dming.dice.random")
    def test_d20_roll(self, mock_random):
        generated_dice = random.randint(1, 20)
        expected_value = generated_dice
        mock_random.randint.return_value = generated_dice

        result = roll("d20")
        self.assertEqual((f"{expected_value}", expected_value), result)

    @patch("dming.dice.random")
    def test_1d20_roll(self, mock_random):
        generated_dice = random.randint(1, 20)
        expected_value = generated_dice
        mock_random.randint.return_value = generated_dice

        result = roll("1d20")
        self.assertEqual((f"{expected_value}", expected_value), result)

    @patch("dming.dice.random")
    def test_6d6_roll(self, mock_random):
        generated_dice = [1, 2, 3, 4, 5, 6, 6]
        expected_value = 21
        mock_random.randint.side_effect = generated_dice

        result = roll("6d6")
        self.assertEqual((f"{expected_value}", expected_value), result)

    @patch("dming.dice.random")
    def test_1d20_plus3_roll(self, mock_random):
        generated_dice = [1, 2, 3, 4, 5, 6, 7]
        mock_random.randint.side_effect = generated_dice

        result = roll("d20+4")
        self.assertEqual(("1+4", 5), result)

    @patch("dming.dice.random")
    def test_2d100_roll(self, mock_random):
        generated_dice = [58, 34, 32]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d100")
        self.assertEqual(("92", 92), result)

    @patch("dming.dice.random")
    def test_1d20_minus3_roll(self, mock_random):
        generated_dice = [20, 19, 18, 17, 16, 15, 14]
        mock_random.randint.side_effect = generated_dice

        result = roll("d20-4")
        self.assertEqual(("20-4", 16), result)

    @patch("dming.dice.random")
    def test_invalid_roll(self, mock_random):
        generated_dice = [1, 2, 3, 4, 5, 6]
        mock_random.randint.side_effect = generated_dice

        with self.assertRaises(Exception) as context:
            roll("xd1")

        self.assertEqual("not allowed characters", f"{context.exception}")


class TestKeepHighestRoll(unittest.TestCase):
    @patch("dming.dice.random")
    def test_2d20kh_roll(self, mock_random):
        generated_dice = [20, 10]
        expected_value = 20
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kh")
        self.assertEqual((f"{expected_value}", expected_value), result)

    @patch("dming.dice.random")
    def test_2d20kh_plus2_roll(self, mock_random):
        generated_dice = [20, 10]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kh+2")
        self.assertEqual(("20+2", 22), result)

    @patch("dming.dice.random")
    def test_2d20kh1_roll(self, mock_random):
        generated_dice = [19, 9]
        expected_value = 19
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kh1")
        self.assertEqual((f"{expected_value}", expected_value), result)

    @patch("dming.dice.random")
    def test_2d20kh1_plus3_roll(self, mock_random):
        generated_dice = [19, 9]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kh1+3")
        self.assertEqual(("19+3", 22), result)

    @patch("dming.dice.random")
    def test_2d20kh1_minus3_roll(self, mock_random):
        generated_dice = [19, 9]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kh1-3")
        self.assertEqual(("19-3", 16), result)

    @patch("dming.dice.random")
    def test_2d20kh1_plus1d20_plus3_roll(self, mock_random):
        generated_dice = [19, 9, 15, 16]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kh1+1d20+3")
        self.assertEqual(("19+15+3", 37), result)


class TestKeepLowestRoll(unittest.TestCase):
    @patch("dming.dice.random")
    def test_2d20kl_roll(self, mock_random):
        generated_dice = [20, 10]
        expected_value = 10
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kl")
        self.assertEqual((f"{expected_value}", expected_value), result)

    @patch("dming.dice.random")
    def test_2d20kl_plus2_roll(self, mock_random):
        generated_dice = [20, 10]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kl+2")
        self.assertEqual(("10+2", 12), result)

    @patch("dming.dice.random")
    def test_2d20kl1_roll(self, mock_random):
        generated_dice = [19, 9]
        expected_value = 9
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kl1")
        self.assertEqual((f"{expected_value}", expected_value), result)

    @patch("dming.dice.random")
    def test_2d20kl1_plus3_roll(self, mock_random):
        generated_dice = [19, 9]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kl1+3")
        self.assertEqual(("9+3", 12), result)

    @patch("dming.dice.random")
    def test_2d20kl1_minus3_roll(self, mock_random):
        generated_dice = [19, 9]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kl1-3")
        self.assertEqual(("9-3", 6), result)

    @patch("dming.dice.random")
    def test_2d20kl1_plus1d20_plus3_roll(self, mock_random):
        generated_dice = [19, 9, 15, 16]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kl1+1d20+3")
        self.assertEqual(("9+15+3", 27), result)
