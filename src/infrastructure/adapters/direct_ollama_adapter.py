"""Módulo que contém o adaptador para usar Ollama diretamente."""
from typing import List, Optional, Dict, Any
from ...domain.use_cases.process_message import AIModel
from .ollama_adapter import OllamaModel


class DirectOllamaModel(AIModel):
    """Adaptador que usa Ollama diretamente quando configurado."""
    
    def __init__(self, model_name: str = "llama2", base_url: str = "http://localhost:11434"):
        """Inicializa o adaptador direto do Ollama.
        
        Args:
            model_name: Nome do modelo Ollama a ser utilizado.
            base_url: URL base do servidor Ollama.
        """
        self.ollama_model = OllamaModel(model_name=model_name, base_url=base_url)
        self.model_name = model_name
        self.base_url = base_url
    
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
            # Verifica se o Ollama está disponível
            if not self.ollama_model.is_available():
                raise Exception("Ollama não está disponível. Verifique se o servidor está rodando.")
            
            # Usa o modelo Ollama
            return self.ollama_model.generate_response(messages, **kwargs)
            
        except Exception as e:
            raise Exception(f"Erro ao usar Ollama diretamente: {str(e)}")
    
    def is_available(self) -> bool:
        """Verifica se o Ollama está disponível."""
        return self.ollama_model.is_available()
    
    def get_available_models(self) -> List[str]:
        """Retorna lista de modelos disponíveis."""
        return self.ollama_model.get_available_models()
    
    def get_status(self) -> str:
        """Retorna o status do Ollama."""
        if self.is_available():
            models = self.get_available_models()
            return f"Ollama funcionando. Modelos disponíveis: {', '.join(models)}"
        else:
            return "Ollama não está disponível" 