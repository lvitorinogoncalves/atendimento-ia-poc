"""Módulo que contém a entidade de mensagem."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """Enum que representa os papéis possíveis em uma mensagem."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Message:
    """Entidade que representa uma mensagem na conversa."""
    role: MessageRole
    content: str
    timestamp: datetime = None

    def __post_init__(self):
        """Inicializa o timestamp com o momento atual se não for fornecido."""
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def to_dict(self) -> dict:
        """Converte a mensagem para um dicionário."""
        return {
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Message':
        """Cria uma instância de Message a partir de um dicionário."""
        return cls(
            role=MessageRole(data["role"]),
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else None
        )
