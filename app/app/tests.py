from django.test import SimpleTestCase

from . import calc
from .calc import even_numbers


class CalcTestCase(SimpleTestCase):
    """Test calc module."""

    def test_add_number(self):
        """Test adding nu,bers together."""
        x = 1
        y = 2

        res = calc.add(x, y)

        self.assertEqual(res, 3)

    def test_list_retun_even_numbers(self):

        # given
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        expected_numbers = [2, 4, 6, 8, 10]

        # when
        res = even_numbers(numbers)

        # then
        self.assertEqual(res, expected_numbers)


