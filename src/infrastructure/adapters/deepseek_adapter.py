"""Módulo que contém o adaptador para a API do DeepSeek."""
from typing import List, Optional, Dict, Any
import os
import requests
from ...domain.use_cases.process_message import AIModel


class DeepSeekModel(AIModel):
    """Implementação do modelo de IA usando a API do DeepSeek."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Inicializa o adaptador do DeepSeek.
        
        Args:
            api_key: Chave da API do DeepSeek. Se não for fornecida, será usada a variável de ambiente DEEPSEEK_API_KEY.
        """
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("A chave da API do DeepSeek não foi fornecida e não foi encontrada nas variáveis de ambiente.")
        
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
    
    def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Gera uma resposta usando a API do DeepSeek.
        
        Args:
            messages: Lista de mensagens no formato esperado pela API do DeepSeek.
            **kwargs: Argumentos adicionais para a API do DeepSeek.
            
        Returns:
            O conteúdo da resposta gerada pelo modelo.
            
        Raises:
            Exception: Em caso de erro na chamada à API.
        """
        try:
            # Configura os parâmetros padrão
            default_kwargs = {
                "model": "deepseek-chat",
                "messages": messages,
                "max_tokens": 150,
                "temperature": 0.7,
            }
            
            # Atualiza com os argumentos fornecidos, se houver
            default_kwargs.update(kwargs)
            
            # Headers para autenticação
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Chama a API
            response = requests.post(
                self.base_url,
                headers=headers,
                json=default_kwargs,
                timeout=30
            )
            
            # Verifica se a resposta foi bem-sucedida
            response.raise_for_status()
            
            # Retorna o conteúdo da resposta
            response_data = response.json()
            return response_data["choices"][0]["message"]["content"].strip()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao chamar a API do DeepSeek: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro inesperado na API do DeepSeek: {str(e)}") 