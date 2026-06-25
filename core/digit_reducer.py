# -*- coding: utf-8 -*-
from typing import List


class DigitReducer:

    """
    Produces digit-sum subdivisions for numbers.
    """

    @staticmethod
    def reduce(number: int) -> List[int]:

        """
        Repeatedly sums the digits of a number
        until a single digit is reached.
        """

        subdivisions = [number]

        while number >= 10:

            number = sum(int(digit) for digit in str(number))
            subdivisions.append(number)

        return subdivisions
