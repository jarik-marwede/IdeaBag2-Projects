#!/usr/bin/env python3
import unittest

from Numbers.Find_Pi_to_the_Nth_digit.find_pi_to_the_nth_digit import get_pi_to


class Test(unittest.TestCase):

    def test_get_pi_to(self):
        self.assertEqual(get_pi_to(10), 3.1415926535)


if __name__ == "__main__":
    unittest.main()
