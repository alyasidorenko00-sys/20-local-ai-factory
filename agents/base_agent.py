"""Базовый класс для всех ИИ-агентов."""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseAgent(ABC):
    """Абстрактный базовый класс для агентов."""

    def __init__(self, agent_id: str, config: Dict = None):
        self.agent_id = agent_id
        self.config = config or {}

    @abstractmethod
    def process(self, input_data: str) -> str:
        """Обработать входные данные и вернуть результат."""
        pass

    def get_status(self) -> Dict[str, Any]:
        """Получить статус агента."""
        return {
            "agent_id": self.agent_id,
            "status": "active",
            "config": self.config
        }