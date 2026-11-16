
from cost_calculator import calculate_cost


def test_ollama_cost():
    cost = calculate_cost(
        "OllamaProvider", "llama3.2", 1000, 2000
    )
    assert cost == 0.0


def test_gemini_cost():
    cost = calculate_cost(
        "GeminiProvider", "gemini-3.8-flash", 1000, 500
    )
    assert cost == 0.0015


def test_unknown_model():
    cost = calculate_cost(
        "GeminiProvider", "unknown-model", 1000, 500
    )
    assert cost is None


def test_zero_tokens():
    cost = calculate_cost(
        "GeminiProvider", "gemini-3.8-flash", 0, 0
    )
    assert cost == 0.0
