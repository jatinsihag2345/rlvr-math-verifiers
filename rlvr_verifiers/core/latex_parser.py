import re
from typing import Optional


class LatexAnswerExtractor:
    """
    Extracts and standardizes mathematical expressions from raw model completions,
    handling standard formats: \\boxed{...}, 'The answer is...', and GSM8K '#### ...'.
    """

    @staticmethod
    def extract_boxed(text: str) -> Optional[str]:
        # Handle nested \boxed{...}
        idx = text.rfind(r"\boxed{")
        if idx == -1:
            return None

        brace_count = 0
        start_idx = idx + len(r"\boxed{")
        for i in range(start_idx, len(text)):
            if text[i] == "{":
                brace_count += 1
            elif text[i] == "}":
                if brace_count == 0:
                    return text[start_idx:i].strip()
                brace_count -= 1
        return None

    @staticmethod
    def extract_gsm8k(text: str) -> Optional[str]:
        match = re.search(r"####\s*(-?[\d\.,]+)", text)
        if match:
            return match.group(1).replace(",", "").strip()
        return None

    @staticmethod
    def extract_answer(text: str) -> Optional[str]:
        # 1. Try \boxed{}
        boxed = LatexAnswerExtractor.extract_boxed(text)
        if boxed is not None:
            return LatexAnswerExtractor.normalize(boxed)

        # 2. Try GSM8K format ####
        gsm = LatexAnswerExtractor.extract_gsm8k(text)
        if gsm is not None:
            return LatexAnswerExtractor.normalize(gsm)

        # 3. Look for phrases like 'The answer is: X' or 'Final Answer: X'
        patterns = [
            r"(?:the\s+answer\s+is|final\s+answer\s+is|answer:)\s*[:\s]*\$?([^\n\.$]+)\$?",
            r"(?:equals|equal\s+to|=)\s*([-\d\./]+)"
        ]
        for p in patterns:
            match = re.search(p, text, re.IGNORECASE)
            if match:
                return LatexAnswerExtractor.normalize(match.group(1).strip())

        return None

    @staticmethod
    def normalize(expr: str) -> str:
        s = expr.strip()
        # Remove trailing periods
        s = s.rstrip(".")
        # Remove LaTeX formatting
        s = s.replace(r"\$", "").replace("$", "")
        s = s.replace(r"\left", "").replace(r"\right", "")
        s = s.replace(r"\%", "%")
        s = s.replace(",", "")  # 1,000 -> 1000

        # Convert fractions \frac{a}{b} -> a/b before stripping braces
        s = re.sub(r"\\frac\{([^\}]+)\}\{([^\}]+)\}", r"\1/\2", s)
        s = re.sub(r"\\dfrac\{([^\}]+)\}\{([^\}]+)\}", r"\1/\2", s)

        s = s.replace(r"\text{", "").replace(r"\mathrm{", "").replace("{", "").replace("}", "")
        return s.strip()
