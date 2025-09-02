"""Módulo que contém o adaptador para o Ollama (IA local)."""
from typing import List, Optional, Dict, Any
import requests
import json
from ...domain.use_cases.process_message import AIModel


class OllamaModel(AIModel):
    """Implementação do modelo de IA usando Ollama local."""
    
    def __init__(self, model_name: str = "llama2", base_url: str = "http://localhost:11434"):
        """Inicializa o adaptador do Ollama.
        
        Args:
            model_name: Nome do modelo Ollama a ser utilizado.
            base_url: URL base do servidor Ollama.
        """
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/chat"
    
    def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Gera uma resposta usando o Ollama local.
        
        Args:
            messages: Lista de mensagens no formato esperado.
            **kwargs: Argumentos adicionais para o modelo.
            
        Returns:
            O conteúdo da resposta gerada pelo modelo.
            
        Raises:
            Exception: Em caso de erro na chamada ao Ollama.
        """
        try:
            # Converte mensagens para o formato do Ollama
            ollama_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    # Ollama não tem role "system", convertemos para "user"
                    ollama_messages.append({
                        "role": "user",
                        "content": f"Instrução do sistema: {msg['content']}"
                    })
                else:
                    ollama_messages.append(msg)
            
            # Prepara a requisição
            payload = {
                "model": self.model_name,
                "messages": ollama_messages,
                "stream": False,
                "options": {
                    "temperature": kwargs.get("temperature", 0.7),
                    "num_predict": kwargs.get("max_tokens", 150)
                }
            }
            
            # Chama a API do Ollama
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=60  # Ollama pode ser mais lento
            )
            
            # Verifica se a resposta foi bem-sucedida
            response.raise_for_status()
            
            # Retorna o conteúdo da resposta
            response_data = response.json()
            return response_data["message"]["content"].strip()
            
        except requests.exceptions.ConnectionError:
            raise Exception("Erro de conexão com Ollama. Verifique se o servidor está rodando.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao chamar o Ollama: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro inesperado no Ollama: {str(e)}")
    
    def is_available(self) -> bool:
        """Verifica se o Ollama está disponível."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_available_models(self) -> List[str]:
        """Retorna lista de modelos disponíveis."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except:
            return [] 