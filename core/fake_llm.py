"""FakeLLM - имитация работы LLM для тестирования без Ollama."""
import random
import time


class FakeLLM:
    """Имитация языковой модели."""

    def __init__(self, model_name="fake-llm"):
        self.model_name = model_name
        self.responses = [
            "Я обработал ваш запрос. Вот результат анализа...",
            "На основе предоставленных данных могу сказать следующее...",
            "Рассматривая проблему с разных сторон, прихожу к выводу...",
            "Мой анализ показывает, что оптимальное решение - это...",
            "С учётом контекста задачи предлагаю следующий подход..."
        ]

    def generate(self, prompt, context=None):
        """Генерирует ответ на основе промпта."""
        time.sleep(0.5)
        base_response = random.choice(self.responses)
        context_info = f" (контекст: {len(context)} записей)" if context else ""
        return f"[{self.model_name}] {base_response}{context_info}\nВаш запрос: {prompt[:50]}..."