import math
from fractions import Fraction
from typing import Optional
from ..core.models import MathProblem, RewardSignal
from ..core.latex_parser import LatexAnswerExtractor


class DeterministicMathVerifier:
    """
    Evaluates model generated mathematical answers against ground truth solutions.
    Provides verifiable reward signals for RL training (PPO, GRPO, DPO).
    """

    def __init__(self, default_tolerance: float = 1e-4):
        self.default_tolerance = default_tolerance

    def verify(self, problem: MathProblem, completion_text: str) -> RewardSignal:
        extracted = LatexAnswerExtractor.extract_answer(completion_text)
        expected = LatexAnswerExtractor.normalize(problem.ground_truth)

        if extracted is None:
            return RewardSignal(
                reward=0.0,
                is_correct=False,
                extracted_answer=None,
                expected_answer=expected,
                error_message="Could not extract boxed or final answer from completion"
            )

        # 1. Direct normalized string match
        if extracted.lower() == expected.lower():
            return RewardSignal(
                reward=1.0,
                is_correct=True,
                extracted_answer=extracted,
                expected_answer=expected
            )

        # 2. Rational number / Fraction equivalence (e.g. 3/6 == 1/2)
        try:
            frac_ext = Fraction(extracted)
            frac_exp = Fraction(expected)
            if frac_ext == frac_exp:
                return RewardSignal(
                    reward=1.0,
                    is_correct=True,
                    extracted_answer=extracted,
                    expected_answer=expected
                )
        except (ValueError, ZeroDivisionError):
            pass

        # 3. Floating point numerical comparison with tolerance
        try:
            val_ext = float(Fraction(extracted) if "/" in extracted else extracted)
            val_exp = float(Fraction(expected) if "/" in expected else expected)
            tolerance = problem.tolerance or self.default_tolerance
            if math.isclose(val_ext, val_exp, rel_tol=tolerance, abs_tol=tolerance):
                return RewardSignal(
                    reward=1.0,
                    is_correct=True,
                    extracted_answer=extracted,
                    expected_answer=expected
                )
        except (ValueError, ZeroDivisionError):
            pass

        return RewardSignal(
            reward=0.0,
            is_correct=False,
            extracted_answer=extracted,
            expected_answer=expected,
            error_message=f"Value mismatch: extracted '{extracted}' != expected '{expected}'"
        )
