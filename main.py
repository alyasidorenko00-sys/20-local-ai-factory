"""Главный файл - запуск МСР сервера."""
from core.orchestrator import Orchestrator
import os


def main():
    print("=" * 60)
    print("  Локальная ИИ-Фабрика (МСР Сервер)")
    print("=" * 60)

    os.makedirs('logs', exist_ok=True)

    orchestrator = Orchestrator(use_ollama=False)

    print("\nОркестратор запущен")
    print("Статус:", orchestrator.get_status())
    print("\nВведите запрос (или 'exit' для выхода):\n")

    try:
        while True:
            user_input = input("Вы: ").strip()

            if user_input.lower() in ['exit', 'quit', 'выход']:
                break

            if not user_input:
                continue

            response = orchestrator.process_input(user_input)
            print(f"\nОркестратор: {response}\n")

    except KeyboardInterrupt:
        print("\nПрервано")
    finally:
        orchestrator.shutdown()
        print("\nРабота завершена")


if __name__ == "__main__":
    main()