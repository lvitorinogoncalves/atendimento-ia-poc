"""Testes para o módulo de configurações."""
import os
import pytest
from unittest.mock import patch, mock_open

from src.infrastructure.config.settings import Settings


class TestSettings:
    """Testes para a classe Settings."""
    
    def test_initialization_with_defaults(self):
        """Testa a inicialização com valores padrão."""
        # Arrange & Act
        settings = Settings()
        
        # Assert
        assert settings.OPENAI_MODEL == "gpt-3.5-turbo"
        assert settings.OPENAI_MAX_TOKENS == 150
        assert settings.OPENAI_TEMPERATURE == 0.7
        assert settings.VOICE_RATE == 150
        assert settings.VOICE_VOLUME == 0.9
        assert settings.VOICE_LANGUAGE == "pt-BR"
        assert settings.SPEECH_ENERGY_THRESHOLD == 300
        assert settings.SPEECH_PAUSE_THRESHOLD == 0.8
        assert settings.APP_NAME == "Atendimento IA"
        assert settings.APP_VERSION == "0.1.0"
        assert settings.DEBUG is False
    
    def test_initialization_with_env_vars(self, monkeypatch):
        """Testa a inicialização com variáveis de ambiente personalizadas."""
        # Arrange
        env_vars = {
            "OPENAI_API_KEY": "test_key",
            "OPENAI_MODEL": "gpt-4",
            "OPENAI_MAX_TOKENS": "200",
            "OPENAI_TEMPERATURE": "0.5",
            "VOICE_RATE": "160",
            "VOICE_VOLUME": "1.0",
            "VOICE_LANGUAGE": "en-US",
            "SPEECH_ENERGY_THRESHOLD": "400",
            "SPEECH_PAUSE_THRESHOLD": "0.5",
            "APP_NAME": "Test App",
            "APP_VERSION": "1.0.0",
            "DEBUG": "True"
        }
        
        for key, value in env_vars.items():
            monkeypatch.setenv(key, value)
        
        # Act
        settings = Settings()
        
        # Assert
        assert settings.OPENAI_API_KEY == "test_key"
        assert settings.OPENAI_MODEL == "gpt-4"
        assert settings.OPENAI_MAX_TOKENS == 200
        assert settings.OPENAI_TEMPERATURE == 0.5
        assert settings.VOICE_RATE == 160
        assert settings.VOICE_VOLUME == 1.0
        assert settings.VOICE_LANGUAGE == "en-US"
        assert settings.SPEECH_ENERGY_THRESHOLD == 400
        assert settings.SPEECH_PAUSE_THRESHOLD == 0.5
        assert settings.APP_NAME == "Test App"
        assert settings.APP_VERSION == "1.0.0"
        assert settings.DEBUG is True
    
    def test_missing_required_env_var(self):
        """Testa a inicialização sem a chave da API obrigatória."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError) as exc_info:
            Settings()
        
        assert "A variável de ambiente OPENAI_API_KEY é obrigatória" in str(exc_info.value)
    
    def test_to_dict_method(self):
        """Testa o método to_dict."""
        # Arrange
        settings = Settings()
        
        # Act
        result = settings.to_dict()
        
        # Assert
        assert isinstance(result, dict)
        assert result["OPENAI_MODEL"] == "gpt-3.5-turbo"
        assert result["OPENAI_MAX_TOKENS"] == 150
        assert result["OPENAI_TEMPERATURE"] == 0.7
        assert result["VOICE_RATE"] == 150
        assert result["VOICE_VOLUME"] == 0.9
        assert result["VOICE_LANGUAGE"] == "pt-BR"
        assert result["SPEECH_ENERGY_THRESHOLD"] == 300
        assert result["SPEECH_PAUSE_THRESHOLD"] == 0.8
        assert result["APP_NAME"] == "Atendimento IA"
        assert result["APP_VERSION"] == "0.1.0"
        assert result["DEBUG"] is False
    
    @patch('os.getenv')
    def test_get_env_variable_with_default(self, mock_getenv):
        """Testa o método _get_env_variable com valor padrão."""
        # Arrange
        mock_getenv.return_value = None
        settings = Settings()
        
        # Act
        result = settings._get_env_variable("TEST_VAR", "default_value")
        
        # Assert
        assert result == "default_value"
    
    @patch('os.getenv')
    def test_get_env_variable_without_default(self, mock_getenv):
        """Testa o método _get_env_variable sem valor padrão."""
        # Arrange
        mock_getenv.return_value = None
        settings = Settings()
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            settings._get_env_variable("REQUIRED_VAR")
        
        assert "A variável de ambiente REQUIRED_VAR é obrigatória" in str(exc_info.value)
    
    @patch('src.infrastructure.config.settings.load_dotenv')
    def test_load_dotenv_called(self, mock_load_dotenv):
        """Testa se load_dotenv é chamado durante a inicialização."""
        # Arrange & Act
        Settings()
        
        # Assert
        mock_load_dotenv.assert_called_once()


def test_settings_singleton():  # pylint: disable=unused-variable
    """Testa se a configuração é um singleton."""
    # Arrange & Act
    from src.infrastructure.config.settings import settings as settings1
    from src.infrastructure.config.settings import settings as settings2
    
    # Assert
    assert settings1 is settings2
    assert id(settings1) == id(settings2)
