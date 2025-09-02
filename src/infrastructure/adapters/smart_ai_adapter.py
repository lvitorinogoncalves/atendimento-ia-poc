"""Módulo que contém um adaptador inteligente que alterna entre diferentes modelos de IA."""
from typing import List, Optional, Dict, Any
from ...domain.use_cases.process_message import AIModel
from .openai_adapter import OpenAIModel
from .deepseek_adapter import DeepSeekModel
from .ollama_adapter import OllamaModel


class SmartAIModel(AIModel):
    """Adaptador inteligente que alterna automaticamente entre OpenAI e DeepSeek."""
    
    def __init__(self, openai_api_key: Optional[str] = None, deepseek_api_key: Optional[str] = None):
        """Inicializa o adaptador inteligente.
        
        Args:
            openai_api_key: Chave da API da OpenAI.
            deepseek_api_key: Chave da API do DeepSeek.
        """
        self.openai_model = OpenAIModel(api_key=openai_api_key)
        self.deepseek_model = DeepSeekModel(api_key=deepseek_api_key)
        self.ollama_model = OllamaModel()
        self.current_model = "openai"  # Começa com OpenAI
        self.fallback_triggered = False
        self.fallback_count = 0
    
    def _is_quota_error(self, error_message: str) -> bool:
        """Verifica se o erro é relacionado a quota excedida."""
        quota_indicators = [
            "quota",
            "insufficient_quota", 
            "rate_limit",
            "billing",
            "payment",
            "429"
        ]
        return any(indicator.lower() in error_message.lower() for indicator in quota_indicators)
    
    def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Gera uma resposta usando o modelo atual, com fallback automático.
        
        Args:
            messages: Lista de mensagens no formato esperado.
            **kwargs: Argumentos adicionais para o modelo.
            
        Returns:
            O conteúdo da resposta gerada pelo modelo.
            
        Raises:
            Exception: Em caso de erro em todos os modelos.
        """
        # Primeira tentativa com o modelo atual
        try:
            if self.current_model == "openai":
                return self.openai_model.generate_response(messages, **kwargs)
            elif self.current_model == "deepseek":
                return self.deepseek_model.generate_response(messages, **kwargs)
            else:
                return self.ollama_model.generate_response(messages, **kwargs)
                
        except Exception as e:
            error_message = str(e)
            
            # Se for erro de quota e ainda não tentamos todos os fallbacks
            if self._is_quota_error(error_message) and self.fallback_count < 2:
                print(f"⚠️  Erro de quota detectado no {self.current_model.upper()}. Tentando próximo modelo...")
                
                # Sequência de fallback: OpenAI -> DeepSeek -> Ollama
                if self.current_model == "openai":
                    self.current_model = "deepseek"
                    print("🔄 Alternando para DeepSeek...")
                elif self.current_model == "deepseek":
                    self.current_model = "ollama"
                    print("🔄 Alternando para Ollama (local)...")
                
                self.fallback_count += 1
                
                # Segunda tentativa com o modelo alternativo
                try:
                    if self.current_model == "openai":
                        return self.openai_model.generate_response(messages, **kwargs)
                    elif self.current_model == "deepseek":
                        return self.deepseek_model.generate_response(messages, **kwargs)
                    else:
                        return self.ollama_model.generate_response(messages, **kwargs)
                        
                except Exception as fallback_error:
                    # Se o segundo modelo falhar, tenta o terceiro
                    if self.fallback_count < 2:
                        if self.current_model == "deepseek":
                            self.current_model = "ollama"
                            print("🔄 Alternando para Ollama (local)...")
                            self.fallback_count += 1
                            
                            try:
                                return self.ollama_model.generate_response(messages, **kwargs)
                            except Exception as ollama_error:
                                raise Exception(f"Todos os modelos falharam. OpenAI: {error_message}, DeepSeek: {str(fallback_error)}, Ollama: {str(ollama_error)}")
                        else:
                            raise Exception(f"Todos os modelos falharam. OpenAI: {error_message}, DeepSeek: {str(fallback_error)}, Ollama: {str(fallback_error)}")
                    else:
                        raise Exception(f"Todos os modelos falharam. OpenAI: {error_message}, DeepSeek: {str(fallback_error)}")
            
            # Se não for erro de quota ou já tentamos todos os fallbacks, propaga o erro
            raise e
    
    def get_current_model_info(self) -> str:
        """Retorna informações sobre o modelo atual."""
        return f"Modelo atual: {self.current_model.upper()}, Fallbacks usados: {self.fallback_count}/2"
    
    def reset_fallback(self) -> None:
        """Reseta o estado de fallback."""
        self.current_model = "openai"
        self.fallback_count = 0 