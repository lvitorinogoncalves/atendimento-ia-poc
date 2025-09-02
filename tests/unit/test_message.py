"""Testes para a entidade Message."""
import pytest
from datetime import datetime
from src.domain.entities.message import Message, MessageRole


def test_create_message():
    """Testa a criação de uma mensagem com valores padrão."""
    # Arrange
    role = MessageRole.USER
    content = "Olá, tudo bem?"
    
    # Act
    message = Message(role=role, content=content)
    
    # Assert
    assert message.role == role
    assert message.content == content
    assert isinstance(message.timestamp, datetime)


def test_create_message_with_timestamp():
    """Testa a criação de uma mensagem com timestamp personalizado."""
    # Arrange
    role = MessageRole.ASSISTANT
    content = "Olá! Como posso ajudar?"
    timestamp = datetime(2023, 1, 1, 12, 0, 0)
    
    # Act
    message = Message(role=role, content=content, timestamp=timestamp)
    
    # Assert
    assert message.role == role
    assert message.content == content
    assert message.timestamp == timestamp


def test_message_to_dict():
    """Testa a conversão de mensagem para dicionário."""
    # Arrange
    role = MessageRole.SYSTEM
    content = "Você é um assistente útil."
    timestamp = datetime(2023, 1, 1, 12, 0, 0)
    message = Message(role=role, content=content, timestamp=timestamp)
    
    # Act
    result = message.to_dict()
    
    # Assert
    assert result == {
        "role": "system",
        "content": "Você é um assistente útil.",
        "timestamp": "2023-01-01T12:00:00"
    }


def test_message_from_dict():
    """Testa a criação de mensagem a partir de um dicionário."""
    # Arrange
    data = {
        "role": "user",
        "content": "Olá, tudo bem?",
        "timestamp": "2023-01-01T12:00:00"
    }
    
    # Act
    message = Message.from_dict(data)
    
    # Assert
    assert message.role == MessageRole.USER
    assert message.content == "Olá, tudo bem?"
    assert message.timestamp == datetime(2023, 1, 1, 12, 0, 0)


def test_message_from_dict_without_timestamp():
    """Testa a criação de mensagem a partir de dicionário sem timestamp."""
    # Arrange
    data = {
        "role": "assistant",
        "content": "Como posso ajudar?"
    }
    
    # Act
    message = Message.from_dict(data)
    
    # Assert
    assert message.role == MessageRole.ASSISTANT
    assert message.content == "Como posso ajudar?"
    assert message.timestamp is not None


def test_message_invalid_role():
    """Testa a criação de mensagem com papel inválido."""
    # Arrange & Act & Assert
    with pytest.raises(ValueError):
        Message(role="invalid_role", content="Teste")


def test_message_empty_content():
    """Testa a criação de mensagem com conteúdo vazio."""
    # Arrange & Act
    message = Message(role=MessageRole.USER, content="")
    
    # Assert
    assert message.content == ""


def test_message_equality():
    """Testa a igualdade entre mensagens."""
    # Arrange
    timestamp = datetime(2023, 1, 1, 12, 0, 0)
    message1 = Message(role=MessageRole.USER, content="Oi", timestamp=timestamp)
    message2 = Message(role=MessageRole.USER, content="Oi", timestamp=timestamp)
    message3 = Message(role=MessageRole.ASSISTANT, content="Oi", timestamp=timestamp)
    
    # Assert
    assert message1 == message2
    assert message1 != message3
    assert message1 != "not a message"


def test_message_repr():
    """Testa a representação em string da mensagem."""
    # Arrange
    message = Message(
        role=MessageRole.USER,
        content="Olá",
        timestamp=datetime(2023, 1, 1, 12, 0, 0)
    )
    
    # Act
    result = repr(message)
    
    # Assert
    assert "Message(" in result
    assert "role=MessageRole.USER" in result
    assert "content='Olá'" in result
    assert "timestamp=datetime.datetime(2023, 1, 1, 12, 0)" in result
