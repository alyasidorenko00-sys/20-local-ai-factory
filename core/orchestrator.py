"""Оркестратор - ядро МСР сервера для управления ИИ-агентами."""
import subprocess
import sys
import os
import logging
from pathlib import Path
from .memory import SharedMemory
from .fake_llm import FakeLLM

# Создаём папку logs ДО настройки логирования
Path('logs').mkdir(exist_ok=True)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('logs/orchestrator.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class Orchestrator:
    """Ядро системы - управляет агентами, памятью и LLM."""

    def __init__(self, use_ollama=False):
        self.use_ollama = use_ollama
        self.memory = SharedMemory()
        self.agents = {}
        self.agent_configs = {}
        self.llm = FakeLLM("fake-llm-v1")

        logger.info("Оркестратор инициализирован")

    def register_agent(self, agent_id, script_path, config=None):
        """Зарегистрировать агента в системе."""
        self.agent_configs[agent_id] = {
            "script_path": script_path,
            "config": config or {},
            "status": "registered"
        }
        logger.info(f"Агент '{agent_id}' зарегистрирован")

    def start_agent(self, agent_id):
        """Запустить агента как подпроцесс."""
        if agent_id not in self.agent_configs:
            return False

        config = self.agent_configs[agent_id]
        script_path = config["script_path"]

        if not os.path.exists(script_path):
            logger.error(f"Скрипт не найден: {script_path}")
            return False

        try:
            process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.agents[agent_id] = process
            config["status"] = "running"
            logger.info(f"Агент '{agent_id}' запущен (PID: {process.pid})")
            return True
        except Exception as e:
            logger.error(f"Ошибка запуска: {e}")
            return False

    def stop_agent(self, agent_id):
        """Остановить агента."""
        if agent_id not in self.agents:
            return False

        try:
            self.agents[agent_id].terminate()
            self.agents[agent_id].wait(timeout=5)
            self.agent_configs[agent_id]["status"] = "stopped"
            del self.agents[agent_id]
            logger.info(f"Агент '{agent_id}' остановлен")
            return True
        except Exception as e:
            logger.error(f"Ошибка остановки: {e}")
            return False

    def process_input(self, user_input):
        """Обработать ввод пользователя."""
        logger.info(f"Получен ввод: {user_input[:50]}...")
        self.memory.add_message("user", user_input)

        response = self.llm.generate(user_input, self.memory.get_history())
        self.memory.add_message("assistant", response, "orchestrator")

        return response

    def get_status(self):
        """Получить статус системы."""
        return {
            "orchestrator": "running",
            "llm_type": "ollama" if self.use_ollama else "fake_llm",
            "agents_count": len(self.agent_configs),
            "running_agents": len(self.agents),
            "memory_size": len(self.memory._messages)
        }

    def shutdown(self):
        """Завершить работу."""
        logger.info("Завершение работы...")
        for agent_id in list(self.agents.keys()):
            self.stop_agent(agent_id)