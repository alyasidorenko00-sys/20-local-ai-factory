"""Тестовый агент-заглушка для проверки работы оркестратора."""
import time
from datetime import datetime


class TestAgent:
    """Простой тестовый агент."""

    def __init__(self):
        self.agent_id = "test-agent"
        print(f"[{datetime.now()}] TestAgent инициализирован")

    def process(self, input_data):
        """Обработка входных данных."""
        print(f"[{datetime.now()}] TestAgent получил: {input_data[:50]}...")
        time.sleep(0.3)
        return f"TestAgent обработал запрос: '{input_data[:30]}...'"


def main():
    """Точка входа для запуска как подпроцесса."""
    agent = TestAgent()
    print("[TestAgent] Готов к работе. Ожидание ввода...")

    try:
        while True:
            line = input()
            if line.strip().lower() == "exit":
                break
            result = agent.process(line)
            print(f"RESULT: {result}")
    except EOFError:
        pass

    print("[TestAgent] Завершение работы")


if __name__ == "__main__":
    main()