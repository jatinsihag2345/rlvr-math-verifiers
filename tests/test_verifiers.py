from rlvr_verifiers.core.models import MathProblem, TaskDomain
from rlvr_verifiers.verifiers.math_verifier import DeterministicMathVerifier
from rlvr_verifiers.core.latex_parser import LatexAnswerExtractor


def test_latex_boxed_extraction():
    text = "After simplifying, we find \\boxed{\\frac{3}{4}} as the answer."
    ans = LatexAnswerExtractor.extract_answer(text)
    assert ans == "3/4"


def test_fraction_equivalence():
    verifier = DeterministicMathVerifier()
    prob = MathProblem(id="t1", domain=TaskDomain.ALGEBRA_MATH, prompt="", ground_truth="1/2")
    res = verifier.verify(prob, "The final answer is \\boxed{\\frac{50}{100}}")
    assert res.is_correct is True
    assert res.reward == 1.0


def test_float_tolerance():
    verifier = DeterministicMathVerifier(default_tolerance=1e-3)
    prob = MathProblem(id="t2", domain=TaskDomain.ALGEBRA_MATH, prompt="", ground_truth="3.14159")
    res = verifier.verify(prob, "Therefore \\boxed{3.1416}")
    assert res.is_correct is True
    assert res.reward == 1.0
