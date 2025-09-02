"""Módulo que contém o adaptador para a API da OpenAI."""
from typing import List, Optional, Dict, Any
import os
from openai import OpenAI

from ...domain.use_cases.process_message import AIModel


class OpenAIModel(AIModel):
    """Implementação do modelo de IA usando a API da OpenAI."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """Inicializa o adaptador da OpenAI.
        
        Args:
            api_key: Chave da API da OpenAI. Se não for fornecida, será usada a variável de ambiente OPENAI_API_KEY.
            model: Nome do modelo da OpenAI a ser utilizado.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("A chave da API da OpenAI não foi fornecida e não foi encontrada nas variáveis de ambiente.")
        
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
    
    def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Gera uma resposta usando a API da OpenAI.
        
        Args:
            messages: Lista de mensagens no formato esperado pela API da OpenAI.
            **kwargs: Argumentos adicionais para a API da OpenAI.
            
        Returns:
            O conteúdo da resposta gerada pelo modelo.
            
        Raises:
            Exception: Em caso de erro na chamada à API.
        """
        try:
            # Configura os parâmetros padrão
            default_kwargs = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 150,
                "temperature": 0.7,
            }
            
            # Atualiza com os argumentos fornecidos, se houver
            default_kwargs.update(kwargs)
            
            # Chama a API
            response = self.client.chat.completions.create(**default_kwargs)
            
            # Retorna o conteúdo da resposta
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Log do erro pode ser implementado aqui
            raise Exception(f"Erro ao chamar a API da OpenAI: {str(e)}")
