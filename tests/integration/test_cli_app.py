"""Testes de integração para a aplicação CLI."""
import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

from src.interface.cli.cli_app import CLIApp


class TestCLIApp:
    """Testes para a aplicação CLI."""
    
    @patch('src.interface.cli.cli_app.VoiceInputAdapter')
    @patch('src.interface.cli.cli_app.VoiceOutputAdapter')
    @patch('src.interface.cli.cli_app.OpenAIModel')
    def test_initialization(self, mock_openai_model, mock_voice_output, mock_voice_input):
        """Testa a inicialização da aplicação CLI."""
        # Arrange
        mock_openai_instance = MagicMock()
        mock_openai_model.return_value = mock_openai_instance
        
        mock_voice_output_instance = MagicMock()
        mock_voice_output.return_value = mock_voice_output_instance
        
        mock_voice_input_instance = MagicMock()
        mock_voice_input.return_value = mock_voice_input_instance
        
        # Act
        app = CLIApp()
        
        # Assert
        assert app is not None
        mock_openai_model.assert_called_once()
        mock_voice_output.assert_called_once()
        mock_voice_input.assert_called_once()
    
    @patch('builtins.input', side_effect=['sair'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_exit_command(self, mock_stdout, mock_input):
        """Testa o comando de sair da aplicação."""
        # Arrange
        app = CLIApp()
        app.voice_output = MagicMock()
        
        # Act
        app.run()
        
        # Assert
        output = mock_stdout.getvalue()
        assert "Atendimento por Voz com IA" in output
        app.voice_output.speak.assert_called_with("Obrigado por utilizar nosso atendimento. Até mais!")
    
    @patch('builtins.input', side_effect=['ajuda', 'sair'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_help_command(self, mock_stdout, mock_input):
        """Testa o comando de ajuda."""
        # Arrange
        app = CLIApp()
        app.voice_output = MagicMock()
        
        # Act
        app.run()
        
        # Assert
        output = mock_stdout.getvalue()
        assert "Comandos disponíveis:" in output
    
    @patch('builtins.input', side_effect=['texto', 'Olá, tudo bem?', 'sair'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_text_command(self, mock_stdout, mock_input):
        """Testa o comando de digitar texto."""
        # Arrange
        app = CLIApp()
        app.voice_output = MagicMock()
        app.process_user_message = MagicMock()
        
        # Act
        app.run()
        
        # Assert
        app.process_user_message.assert_called_once_with("Olá, tudo bem?")
    
    @patch('builtins.input', side_effect=['fale', 'sair'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_voice_command_success(self, mock_stdout, mock_input):
        """Testa o comando de fala com sucesso."""
        # Arrange
        app = CLIApp()
        app.voice_output = MagicMock()
        app.voice_input = MagicMock()
        app.voice_input.listen.return_value = (True, "Olá, como vai?")
        app.process_user_message = MagicMock()
        
        # Act
        app.run()
        
        # Assert
        app.voice_input.listen.assert_called_once()
        app.process_user_message.assert_called_once_with("Olá, como vai?")
    
    @patch('builtins.input', side_effect=['fale', 'sair'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_voice_command_error(self, mock_stdout, mock_input):
        """Testa o comando de fala com erro."""
        # Arrange
        app = CLIApp()
        app.voice_output = MagicMock()
        app.voice_input = MagicMock()
        app.voice_input.listen.return_value = (False, "Erro ao reconhecer fala")
        app.process_user_message = MagicMock()
        
        # Act
        app.run()
        
        # Assert
        app.voice_input.listen.assert_called_once()
        app.process_user_message.assert_not_called()
    
    @patch('builtins.input', side_effect=['historico', 'sair'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_history_command_empty(self, mock_stdout, mock_input):
        """Testa o comando de histórico vazio."""
        # Arrange
        app = CLIApp()
        app.voice_output = MagicMock()
        app.conversation_history = []
        
        # Act
        app.run()
        
        # Assert
        output = mock_stdout.getvalue()
        assert "Nenhuma mensagem no histórico." in output
    
    @patch('builtins.input', side_effect=['limpar', 'sair'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_clear_command(self, mock_stdout, mock_input):
        """Testa o comando de limpar histórico."""
        # Arrange
        app = CLIApp()
        app.voice_output = MagicMock()
        app.conversation_history = ["mensagem 1", "mensagem 2"]
        
        # Act
        app.run()
        
        # Assert
        assert len(app.conversation_history) == 0
        output = mock_stdout.getvalue()
        assert "Histórico da conversa limpo com sucesso!" in output
    
    @patch('builtins.input', side_effect=['comando_invalido', 'sair'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_command(self, mock_stdout, mock_input):
        """Testa um comando inválido."""
        # Arrange
        app = CLIApp()
        app.voice_output = MagicMock()
        
        # Act
        app.run()
        
        # Assert
        output = mock_stdout.getvalue()
        assert "Comando não reconhecido" in output
    
    @patch('builtins.input', side_effect=KeyboardInterrupt())
    def test_keyboard_interrupt(self, mock_input):
        """Testa o tratamento de interrupção por teclado."""
        # Arrange
        app = CLIApp()
        app.voice_output = MagicMock()
        
        # Act
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            app.run()
        
        # Assert
        app.voice_output.speak.assert_called_with("Atendimento interrompido.")
