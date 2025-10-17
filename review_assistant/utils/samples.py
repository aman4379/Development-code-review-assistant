from typing import Dict


def load_sample_code_snippets() -> Dict[str, str]:
    return {
        "python": """
import math

def area(r):
    # bad naming and no docstring
    if r == 0:
        return 0
    return math.pi * r * r

print(area(2))
""".strip(),
        "javascript": """
function add(a, b){
    // no type checks
    return a + b
}
console.log(add(1, '2'))
""".strip(),
    }


def load_standards_text() -> str:
    return """
Python: Follow PEP 8, use meaningful names, add docstrings for public functions, avoid bare except, handle errors explicitly, write small functions, and add type hints for clarity.
JavaScript/TypeScript: Use ESLint recommended rules, avoid implicit any, prefer const, validate inputs, and avoid console.log in production.
Security: avoid eval and dynamic code execution, sanitize external inputs, and prefer parameterized queries for DB access.
""".strip()
