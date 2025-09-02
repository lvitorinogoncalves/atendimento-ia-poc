"""Testes de integração para os adaptadores de voz."""
import pytest
from unittest.mock import patch, MagicMock

from src.infrastructure.adapters.voice_input import VoiceInputAdapter, VoiceInputError
from src.infrastructure.adapters.voice_output import VoiceOutputAdapter, VoiceOutputError


class TestVoiceInputAdapter:
    """Testes para o adaptador de entrada de voz."""
    
    @patch('src.infrastructure.adapters.voice_input.sr')
    def test_listen_success(self, mock_sr):
        """Testa o reconhecimento de voz bem-sucedido."""
        # Arrange
        mock_recognizer = MagicMock()
        mock_audio = MagicMock()
        mock_sr.Recognizer.return_value = mock_recognizer
        mock_sr.Microphone.return_value = MagicMock()
        
        # Configura o reconhecedor para retornar um áudio reconhecido
        mock_recognizer.recognize_google.return_value = "Olá, tudo bem?"
        
        adapter = VoiceInputAdapter()
        
        # Act
        success, text = adapter.listen()
        
        # Assert
        assert success is True
        assert text == "Olá, tudo bem?"
    
    @patch('src.infrastructure.adapters.voice_input.sr')
    def test_listen_unknown_value_error(self, mock_sr):
        """Testa o tratamento de erro quando o áudio não é reconhecido."""
        # Arrange
        mock_recognizer = MagicMock()
        mock_audio = MagicMock()
        mock_sr.Recognizer.return_value = mock_recognizer
        mock_sr.Microphone.return_value = MagicMock()
        
        # Configura o reconhecedor para levantar UnknownValueError
        from speech_recognition import UnknownValueError
        mock_recognizer.recognize_google.side_effect = UnknownValueError()
        
        adapter = VoiceInputAdapter()
        
        # Act
        success, text = adapter.listen()
        
        # Assert
        assert success is False
        assert "Não foi possível entender o áudio" in text
    
    @patch('src.infrastructure.adapters.voice_input.sr')
    def test_listen_request_error(self, mock_sr):
        """Testa o tratamento de erro na requisição ao serviço de reconhecimento."""
        # Arrange
        mock_recognizer = MagicMock()
        mock_audio = MagicMock()
        mock_sr.Recognizer.return_value = mock_recognizer
        mock_sr.Microphone.return_value = MagicMock()
        
        # Configura o reconhecedor para levantar RequestError
        from speech_recognition import RequestError
        mock_recognizer.recognize_google.side_effect = RequestError("Erro na API")
        
        adapter = VoiceInputAdapter()
        
        # Act
        success, text = adapter.listen()
        
        # Assert
        assert success is False
        assert "Erro ao acessar o serviço de reconhecimento de fala" in text


class TestVoiceOutputAdapter:
    """Testes para o adaptador de saída de voz."""
    
    @patch('src.infrastructure.adapters.voice_output.pyttsx3')
    def test_speak_success(self, mock_pyttsx3):
        """Testa a fala de um texto com sucesso."""
        # Arrange
        mock_engine = MagicMock()
        mock_pyttsx3.init.return_value = mock_engine
        
        # Configura a propriedade voices para retornar uma lista de vozes
        mock_voice = MagicMock()
        mock_voice.languages = ['pt_BR']
        mock_engine.getProperty.return_value = [mock_voice]
        
        adapter = VoiceOutputAdapter()
        
        # Act
        adapter.speak("Olá, como vai?")
        
        # Assert
        mock_engine.say.assert_called_once_with("Olá, como vai?")
        mock_engine.runAndWait.assert_called_once()
    
    @patch('src.infrastructure.adapters.voice_output.pyttsx3')
    def test_speak_error(self, mock_pyttsx3):
        """Testa o tratamento de erro ao falar um texto."""
        # Arrange
        mock_engine = MagicMock()
        mock_pyttsx3.init.return_value = mock_engine
        
        # Configura o engine para levantar uma exceção
        mock_engine.say.side_effect = Exception("Erro ao falar")
        
        adapter = VoiceOutputAdapter()
        
        # Act & Assert
        with pytest.raises(VoiceOutputError) as exc_info:
            adapter.speak("Olá, como vai?")
        
        assert "Erro ao tentar falar o texto" in str(exc_info.value)
    
    @patch('src.infrastructure.adapters.voice_output.pyttsx3')
    def test_set_voice_success(self, mock_pyttsx3):
        """Testa a definição de uma voz específica."""
        # Arrange
        mock_engine = MagicMock()
        mock_pyttsx3.init.return_value = mock_engine
        
        # Configura as vozes disponíveis
        mock_voice1 = MagicMock()
        mock_voice1.id = "voice1"
        mock_voice2 = MagicMock()
        mock_voice2.id = "voice2"
        mock_engine.getProperty.return_value = [mock_voice1, mock_voice2]
        
        adapter = VoiceOutputAdapter()
        
        # Act
        result = adapter.set_voice("voice2")
        
        # Assert
        assert result is True
        mock_engine.setProperty.assert_called_once_with('voice', 'voice2')
    
    @patch('src.infrastructure.adapters.voice_output.pyttsx3')
    def test_set_voice_not_found(self, mock_pyttsx3):
        """Testa a tentativa de definir uma voz que não existe."""
        # Arrange
        mock_engine = MagicMock()
        mock_pyttsx3.init.return_value = mock_engine
        
        # Configura as vozes disponíveis
        mock_voice = MagicMock()
        mock_voice.id = "voice1"
        mock_engine.getProperty.return_value = [mock_voice]
        
        adapter = VoiceOutputAdapter()
        
        # Act
        result = adapter.set_voice("nonexistent_voice")
        
        # Assert
        assert result is False
        mock_engine.setProperty.assert_not_called()
    
    @patch('src.infrastructure.adapters.voice_output.pyttsx3')
    def test_get_available_voices(self, mock_pyttsx3):
        """Testa a listagem de vozes disponíveis."""
        # Arrange
        mock_engine = MagicMock()
        mock_pyttsx3.init.return_value = mock_engine
        
        # Configura as vozes disponíveis
        mock_voice1 = MagicMock()
        mock_voice1.id = "voice1"
        mock_voice1.name = "Voz 1"
        mock_voice1.languages = ["pt_BR"]
        mock_voice1.gender = "female"
        
        mock_voice2 = MagicMock()
        mock_voice2.id = "voice2"
        mock_voice2.name = "Voz 2"
        mock_voice2.languages = ["en_US"]
        mock_voice2.gender = "male"
        
        mock_engine.getProperty.return_value = [mock_voice1, mock_voice2]
        
        adapter = VoiceOutputAdapter()
        
        # Act
        voices = adapter.get_available_voices()
        
        # Assert
        assert len(voices) == 2
        assert voices[0]["id"] == "voice1"
        assert voices[0]["name"] == "Voz 1"
        assert voices[0]["languages"] == ["pt_BR"]
        assert voices[0]["gender"] == "female"
        
        assert voices[1]["id"] == "voice2"
        assert voices[1]["name"] == "Voz 2"
        assert voices[1]["languages"] == ["en_US"]
        assert voices[1]["gender"] == "male"
