"""Общая память агентов - хранилище контекста и истории."""
from datetime import datetime


class SharedMemory:
    """Общая память для всех агентов системы."""

    def __init__(self):
        self._messages = []
        self._context = {}
        self._agent_states = {}

    def add_message(self, role, content, agent_id="user"):
        """Добавить сообщение в историю."""
        self._messages.append({
            "role": role,
            "content": content,
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat()
        })

    def get_history(self, limit=10):
        """Получить историю сообщений."""
        return self._messages[-limit:]

    def set_context(self, key, value):
        """Установить контекстную переменную."""
        self._context[key] = value

    def get_context(self, key, default=None):
        """Получить контекстную переменную."""
        return self._context.get(key, default)

    def clear(self):
        """Очистить всю память."""
        self._messages.clear()
        self._context.clear()
        self._agent_states.clear()