from django.test import SimpleTestCase

from . import calc


class CalcTestCase(SimpleTestCase):
    """Test calc module."""

    def test_add_number(self):
        """Test adding nu,bers together."""
        x = 1
        y = 2

        res = calc.add(x, y)

        self.assertEqual(res, 3)
