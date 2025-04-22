import sys
import json
import argparse
from .core.models import MathProblem, TaskDomain
from .verifiers.math_verifier import DeterministicMathVerifier


def test_sample_verification():
    verifier = DeterministicMathVerifier()
    test_cases = [
        ("Janet has 16 eggs... \\boxed{18}", "18", True),
        ("Solving the equation gives #### 9", "9", True),
        ("The area is equal to 30", "30", True),
        ("The probability is \\boxed{\\frac{2}{12}}", "1/6", True),
        ("The remainder is \\boxed{3}", "1", False)
    ]

    print("\nRunning Deterministic Math Verifier Test Suite:")
    print("=" * 65)
    all_passed = True
    for text, expected, should_pass in test_cases:
        prob = MathProblem(id="test", domain=TaskDomain.GSM8K_ARITHMETIC, prompt="", ground_truth=expected)
        res = verifier.verify(prob, text)
        matched = (res.is_correct == should_pass)
        status = "PASSED" if matched else "FAILED"
        print(f" -> [{status}] Extracted: '{res.extracted_answer}' | Expected: '{res.expected_answer}' | Reward: {res.reward}")
        if not matched:
            all_passed = False

    print("=" * 65)
    if all_passed:
        print("All test cases verified successfully!\n")
    else:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="RLVR Math Verifiers CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("test", help="Run verifier test suite")

    args = parser.parse_args()
    if args.command == "test":
        test_sample_verification()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
