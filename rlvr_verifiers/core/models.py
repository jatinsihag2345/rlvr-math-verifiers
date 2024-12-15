from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from enum import Enum


class TaskDomain(str, Enum):
    GSM8K_ARITHMETIC = "gsm8k_arithmetic"
    ALGEBRA_MATH = "algebra_math"
    NUMBER_THEORY = "number_theory"
    GEOMETRY = "geometry"
    PROBABILITY = "probability"


@dataclass
class MathProblem:
    id: str
    domain: TaskDomain
    prompt: str
    ground_truth: str
    difficulty: int = 1  # 1 to 5 scale
    tolerance: float = 1e-5


@dataclass
class RewardSignal:
    reward: float  # Binary 0.0 or 1.0, or partial step reward
    is_correct: bool
    extracted_answer: Optional[str]
    expected_answer: str
    error_message: Optional[str] = None
    step_rewards: List[float] = field(default_factory=list)
