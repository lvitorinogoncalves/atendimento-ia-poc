"""Módulo de configuração da aplicação."""
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class Settings:
    """Classe de configuração da aplicação."""
    
    def __init__(self):
        """Inicializa as configurações carregando as variáveis de ambiente."""
        # Carrega as variáveis de ambiente do arquivo .env
        load_dotenv()
        
        # Configurações da API da OpenAI
        self.OPENAI_API_KEY: str = self._get_env_variable("OPENAI_API_KEY")
        self.OPENAI_MODEL: str = self._get_env_variable("OPENAI_MODEL", "gpt-3.5-turbo")
        self.OPENAI_MAX_TOKENS: int = int(self._get_env_variable("OPENAI_MAX_TOKENS", "150"))
        self.OPENAI_TEMPERATURE: float = float(self._get_env_variable("OPENAI_TEMPERATURE", "0.7"))
        
        # Configurações da API do DeepSeek
        self.DEEPSEEK_API_KEY: str = self._get_env_variable("DEEPSEEK_API_KEY", "")
        
        # Configurações do Ollama
        self.OLLAMA_ENABLED: bool = self._get_env_variable("OLLAMA_ENABLED", "False").lower() == "true"
        self.OLLAMA_MODEL: str = self._get_env_variable("OLLAMA_MODEL", "llama2")
        self.OLLAMA_BASE_URL: str = self._get_env_variable("OLLAMA_BASE_URL", "http://localhost:11434")
        
        # Configurações de voz
        self.VOICE_RATE: int = int(self._get_env_variable("VOICE_RATE", "150"))
        self.VOICE_VOLUME: float = float(self._get_env_variable("VOICE_VOLUME", "0.9"))
        self.VOICE_LANGUAGE: str = self._get_env_variable("VOICE_LANGUAGE", "pt-BR")
        
        # Configurações do reconhecimento de fala
        self.SPEECH_ENERGY_THRESHOLD: int = int(self._get_env_variable("SPEECH_ENERGY_THRESHOLD", "300"))
        self.SPEECH_PAUSE_THRESHOLD: float = float(self._get_env_variable("SPEECH_PAUSE_THRESHOLD", "0.8"))
        
        # Configurações da aplicação
        self.APP_NAME: str = self._get_env_variable("APP_NAME", "Atendimento IA")
        self.APP_VERSION: str = self._get_env_variable("APP_VERSION", "0.1.0")
        self.DEBUG: bool = self._get_env_variable("DEBUG", "False").lower() == "true"
    
    def _get_env_variable(self, key: str, default: Optional[str] = None) -> str:
        """Obtém uma variável de ambiente ou retorna um valor padrão.
        
        Args:
            key: Nome da variável de ambiente.
            default: Valor padrão a ser retornado se a variável não existir.
            
        Returns:
            O valor da variável de ambiente ou o valor padrão.
            
        Raises:
            ValueError: Se a variável for obrigatória (sem valor padrão) e não estiver definida.
        """
        value = os.getenv(key, default)
        if value is None:
            raise ValueError(f"A variável de ambiente {key} é obrigatória e não foi definida.")
        return value
    
    def to_dict(self) -> Dict[str, Any]:
        """Retorna as configurações como um dicionário.
        
        Returns:
            Dicionário com as configurações.
        """
        return {
            # OpenAI
            "OPENAI_MODEL": self.OPENAI_MODEL,
            "OPENAI_MAX_TOKENS": self.OPENAI_MAX_TOKENS,
            "OPENAI_TEMPERATURE": self.OPENAI_TEMPERATURE,
            
            # DeepSeek
            "DEEPSEEK_API_KEY": "***" if self.DEEPSEEK_API_KEY else "Não configurado",
            
            # Ollama
            "OLLAMA_ENABLED": self.OLLAMA_ENABLED,
            "OLLAMA_MODEL": self.OLLAMA_MODEL,
            "OLLAMA_BASE_URL": self.OLLAMA_BASE_URL,
            
            # Voz
            "VOICE_RATE": self.VOICE_RATE,
            "VOICE_VOLUME": self.VOICE_VOLUME,
            "VOICE_LANGUAGE": self.VOICE_LANGUAGE,
            
            # Reconhecimento de fala
            "SPEECH_ENERGY_THRESHOLD": self.SPEECH_ENERGY_THRESHOLD,
            "SPEECH_PAUSE_THRESHOLD": self.SPEECH_PAUSE_THRESHOLD,
            
            # Aplicação
            "APP_NAME": self.APP_NAME,
            "APP_VERSION": self.APP_VERSION,
            "DEBUG": self.DEBUG,
        }


# Instância global de configurações
settings = Settings()
