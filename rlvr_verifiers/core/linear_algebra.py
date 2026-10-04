from typing import List, Union


class LinearAlgebraVerifier:
    """
    Validates vector and matrix equality for linear algebra reasoning benchmarks.
    """

    @staticmethod
    def verify_vector(v1: List[Union[int, float]], v2: List[Union[int, float]], tolerance: float = 1e-5) -> bool:
        if len(v1) != len(v2):
            return False
        return all(abs(a - b) <= tolerance for a, b in zip(v1, v2))

    @staticmethod
    def verify_matrix(m1: List[List[Union[int, float]]], m2: List[List[Union[int, float]]], tolerance: float = 1e-5) -> bool:
        if len(m1) != len(m2):
            return False
        for r1, r2 in zip(m1, m2):
            if len(r1) != len(r2) or not all(abs(a - b) <= tolerance for a, b in zip(r1, r2)):
                return False
        return True
