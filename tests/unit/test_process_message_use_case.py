"""Testes para o caso de uso de processamento de mensagens."""
import pytest
from unittest.mock import Mock
from datetime import datetime

from src.domain.entities.message import Message, MessageRole
from src.domain.use_cases.process_message import (
    ProcessMessageUseCase,
    ProcessMessageInput,
    ProcessMessageOutput,
    AIModel,
)


class MockAIModel(AIModel):
    """Implementação mock do modelo de IA para testes."""
    
    def __init__(self, response: str = "Resposta padrão"):
        """Inicializa o mock com uma resposta padrão."""
        self.response = response
        self.last_messages = None
        self.last_kwargs = None
    
    def generate_response(self, messages: list, **kwargs) -> str:
        """Método mock que retorna uma resposta predefinida."""
        self.last_messages = messages
        self.last_kwargs = kwargs
        return self.response


def test_process_message_use_case_initialization():
    """Testa a inicialização do caso de uso."""
    # Arrange
    mock_ai_model = MockAIModel()
    
    # Act
    use_case = ProcessMessageUseCase(ai_model=mock_ai_model)
    
    # Assert
    assert use_case is not None


def test_process_message_with_history():
    """Testa o processamento de mensagem com histórico."""
    # Arrange
    mock_ai_model = MockAIModel(response="Resposta da IA")
    use_case = ProcessMessageUseCase(ai_model=mock_ai_model)
    
    # Criar histórico de conversa
    history = [
        Message(role=MessageRole.USER, content="Olá", timestamp=datetime(2023, 1, 1, 12, 0, 0)),
        Message(role=MessageRole.ASSISTANT, content="Olá! Como posso ajudar?", timestamp=datetime(2023, 1, 1, 12, 0, 5)),
    ]
    
    input_data = ProcessMessageInput(
        user_message="Quero fazer um pedido",
        conversation_history=history,
        model_kwargs={"temperature": 0.7}
    )
    
    # Act
    output = use_case.execute(input_data)
    
    # Assert
    assert isinstance(output, ProcessMessageOutput)
    assert output.response == "Resposta da IA"
    assert output.user_message.role == MessageRole.USER
    assert output.user_message.content == "Quero fazer um pedido"
    assert output.assistant_message.role == MessageRole.ASSISTANT
    assert output.assistant_message.content == "Resposta da IA"
    
    # Verifica se o modelo foi chamado com os parâmetros corretos
    assert len(mock_ai_model.last_messages) == 4  # system + 2 históricos + user message
    assert mock_ai_model.last_messages[0]["role"] == "system"
    assert mock_ai_model.last_messages[1]["content"] == "Olá"
    assert mock_ai_model.last_messages[2]["content"] == "Olá! Como posso ajudar?"
    assert mock_ai_model.last_messages[3]["content"] == "Quero fazer um pedido"
    
    # Verifica se os kwargs foram passados corretamente
    assert mock_ai_model.last_kwargs["temperature"] == 0.7


def test_process_message_without_history():
    """Testa o processamento de mensagem sem histórico."""
    # Arrange
    mock_ai_model = MockAIModel(response="Primeira resposta")
    use_case = ProcessMessageUseCase(ai_model=mock_ai_model)
    
    input_data = ProcessMessageInput(
        user_message="Olá",
        conversation_history=[]
    )
    
    # Act
    output = use_case.execute(input_data)
    
    # Assert
    assert output.response == "Primeira resposta"
    assert len(mock_ai_model.last_messages) == 2  # system + user message


def test_process_message_with_max_history():
    """Testa o limite de histórico de mensagens."""
    # Arrange
    mock_ai_model = MockAIModel()
    use_case = ProcessMessageUseCase(ai_model=mock_ai_model)
    
    # Criar um histórico maior que o limite padrão (4 mensagens)
    history = [
        Message(role=MessageRole.USER, content=f"Mensagem {i}")
        for i in range(10)  # 10 mensagens no total
    ]
    
    input_data = ProcessMessageInput(
        user_message="Nova mensagem",
        conversation_history=history,
        max_history=2  # Limitar a 2 iterações (4 mensagens: 2 user + 2 assistant)
    )
    
    # Act
    use_case.execute(input_data)
    
    # Assert - Deve manter apenas as últimas 4 mensagens do histórico (2 user + 2 assistant)
    assert len(mock_ai_model.last_messages) == 5  # system + 4 do histórico


def test_process_message_with_custom_system_prompt():
    """Testa o uso de um prompt de sistema personalizado."""
    # Arrange
    mock_ai_model = MockAIModel()
    use_case = ProcessMessageUseCase(ai_model=mock_ai_model)
    
    input_data = ProcessMessageInput(
        user_message="Olá",
        conversation_history=[],
        model_kwargs={
            "system_prompt": "Você é um assistente de vendas."
        }
    )
    
    # Act
    use_case.execute(input_data)
    
    # Assert
    assert mock_ai_model.last_messages[0]["content"] == "Você é um assistente de vendas."


def test_process_message_error_handling():
    """Testa o tratamento de erros ao processar mensagem."""
    # Arrange
    mock_ai_model = Mock(spec=AIModel)
    mock_ai_model.generate_response.side_effect = Exception("Erro na API")
    
    use_case = ProcessMessageUseCase(ai_model=mock_ai_model)
    
    input_data = ProcessMessageInput(
        user_message="Olá",
        conversation_history=[]
    )
    
    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        use_case.execute(input_data)
    
    assert "Erro na API" in str(exc_info.value)
