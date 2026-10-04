import math
from typing import Tuple, Optional


class SymbolicFractionReducer:
    """
    Utility for reducing rational mathematical expressions and comparing
    unsimplified fractions against canonical ground truth representations.
    """

    @staticmethod
    def reduce_fraction(numerator: int, denominator: int) -> Tuple[int, int]:
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero.")
        common = math.gcd(numerator, denominator)
        num = numerator // common
        den = denominator // common
        if den < 0:
            num = -num
            den = -den
        return num, den

    @staticmethod
    def are_fractions_equivalent(num1: int, den1: int, num2: int, den2: int) -> bool:
        try:
            r1 = SymbolicFractionReducer.reduce_fraction(num1, den1)
            r2 = SymbolicFractionReducer.reduce_fraction(num2, den2)
            return r1 == r2
        except ZeroDivisionError:
            return False
