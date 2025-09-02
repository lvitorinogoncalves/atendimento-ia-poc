"""Testes de integração para o adaptador da OpenAI."""
import os
import pytest
from unittest.mock import patch, MagicMock

from src.infrastructure.adapters.openai_adapter import OpenAIModel


@pytest.fixture
def mock_openai_client():
    """Fixture para mock do cliente da OpenAI."""
    with patch('src.infrastructure.adapters.openai_adapter.OpenAI') as mock_openai:
        yield mock_openai


def test_openai_adapter_initialization():
    """Testa a inicialização do adaptador da OpenAI."""
    # Arrange & Act
    adapter = OpenAIModel(api_key="test_key")
    
    # Assert
    assert adapter is not None
    assert adapter.model == "gpt-3.5-turbo"


def test_generate_response_success(mock_openai_client):
    """Testa a geração de resposta bem-sucedida."""
    # Arrange
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    
    mock_message.content = "Resposta de teste"
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    
    mock_client_instance = MagicMock()
    mock_chat = MagicMock()
    mock_completions = MagicMock()
    
    mock_completions.create.return_value = mock_response
    mock_chat.completions = mock_completions
    mock_client_instance.chat = mock_chat
    mock_openai_client.return_value = mock_client_instance
    
    adapter = OpenAIModel(api_key="test_key")
    
    # Act
    response = adapter.generate_response(
        messages=[{"role": "user", "content": "Olá"}],
        temperature=0.7,
        max_tokens=100
    )
    
    # Assert
    assert response == "Resposta de teste"
    mock_completions.create.assert_called_once()
    
    # Verifica se os parâmetros foram passados corretamente
    call_args = mock_completions.create.call_args[1]
    assert call_args["model"] == "gpt-3.5-turbo"
    assert call_args["messages"] == [{"role": "user", "content": "Olá"}]
    assert call_args["temperature"] == 0.7
    assert call_args["max_tokens"] == 100


def test_generate_response_error_handling(mock_openai_client):
    """Testa o tratamento de erros na geração de resposta."""
    # Arrange
    mock_client_instance = MagicMock()
    mock_chat = MagicMock()
    mock_completions = MagicMock()
    
    mock_completions.create.side_effect = Exception("Erro na API")
    mock_chat.completions = mock_completions
    mock_client_instance.chat = mock_chat
    mock_openai_client.return_value = mock_client_instance
    
    adapter = OpenAIModel(api_key="test_key")
    
    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        adapter.generate_response(messages=[{"role": "user", "content": "Olá"}])
    
    assert "Erro na API" in str(exc_info.value)


def test_default_model_used_when_not_specified():
    """Testa se o modelo padrão é usado quando nenhum é especificado."""
    # Arrange & Act
    adapter = OpenAIModel(api_key="test_key")
    
    # Assert
    assert adapter.model == "gpt-3.5-turbo"


def test_custom_model_used_when_specified():
    """Testa se o modelo personalizado é usado quando especificado."""
    # Arrange & Act
    adapter = OpenAIModel(api_key="test_key", model="gpt-4")
    
    # Assert
    assert adapter.model == "gpt-4"


def test_api_key_from_environment_variable(monkeypatch):
    """Testa se a chave da API é obtida da variável de ambiente."""
    # Arrange
    test_api_key = "test_env_key"
    monkeypatch.setenv("OPENAI_API_KEY", test_api_key)
    
    # Act
    adapter = OpenAIModel()
    
    # Assert
    assert adapter.api_key == test_api_key


def test_missing_api_key_raises_error():
    """Testa se uma exceção é lançada quando a chave da API não está definida."""
    # Arrange & Act & Assert
    with pytest.raises(ValueError) as exc_info:
        OpenAIModel(api_key="")
    
    assert "A chave da API da OpenAI" in str(exc_info.value)
