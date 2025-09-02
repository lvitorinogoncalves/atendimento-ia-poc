"""Módulo que contém o caso de uso para processar mensagens com IA."""
from typing import List, Optional
from dataclasses import dataclass

from ..entities.message import Message, MessageRole


class AIModel:
    """Interface para modelos de IA."""
    
    def generate_response(self, messages: List[dict], **kwargs) -> str:
        """Gera uma resposta com base nas mensagens fornecidas.
        
        Args:
            messages: Lista de mensagens no formato esperado pelo modelo.
            **kwargs: Argumentos adicionais para o modelo.
            
        Returns:
            A resposta gerada pelo modelo.
        """
        raise NotImplementedError


@dataclass
class ProcessMessageInput:
    """Dados de entrada para o caso de uso de processamento de mensagem."""
    user_message: str
    conversation_history: List[Message]
    max_history: int = 4
    model_kwargs: Optional[dict] = None


@dataclass
class ProcessMessageOutput:
    """Dados de saída do caso de uso de processamento de mensagem."""
    response: str
    user_message: Message
    assistant_message: Message


class ProcessMessageUseCase:
    """Caso de uso para processar mensagens com IA."""
    
    def __init__(self, ai_model: AIModel):
        """Inicializa o caso de uso com o modelo de IA.
        
        Args:
            ai_model: Instância do modelo de IA que implementa a interface AIModel.
        """
        self.ai_model = ai_model
    
    def execute(self, input_data: ProcessMessageInput) -> ProcessMessageOutput:
        """Executa o processamento da mensagem.
        
        Args:
            input_data: Dados de entrada para o processamento.
            
        Returns:
            Os dados de saída com a resposta processada.
        """
        # Cria a mensagem do usuário
        user_message = Message(
            role=MessageRole.USER,
            content=input_data.user_message
        )
        
        # Prepara o histórico de mensagens para o modelo
        messages = [
            {"role": "system", "content": "Você é um assistente virtual de atendimento telefônico. Seja prestativo e objetivo."}
        ]
        
        # Adiciona o histórico da conversa (limitado pelo max_history)
        for msg in input_data.conversation_history[-(input_data.max_history * 2):]:
            messages.append({"role": msg.role.value, "content": msg.content})
        
        # Adiciona a mensagem atual do usuário
        messages.append({"role": "user", "content": input_data.user_message})
        
        # Gera a resposta usando o modelo de IA
        model_kwargs = input_data.model_kwargs or {}
        response = self.ai_model.generate_response(messages, **model_kwargs)
        
        # Cria a mensagem do assistente
        assistant_message = Message(
            role=MessageRole.ASSISTANT,
            content=response
        )
        
        return ProcessMessageOutput(
            response=response,
            user_message=user_message,
            assistant_message=assistant_message
        )
