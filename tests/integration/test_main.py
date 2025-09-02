"""Testes de integração para o módulo principal."""
import sys
from unittest.mock import patch, MagicMock
from io import StringIO


def test_main_success():
    """Testa a execução bem-sucedida do módulo principal."""
    # Arrange
    with patch('src.interface.cli.cli_app.main') as mock_main:
        mock_main.return_value = 0
        
        # Redireciona a saída padrão
        original_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # Act
            with patch.object(sys, 'argv', ['main.py']):
                from main import main
                return_code = main()
                
            # Assert
            assert return_code == 0
            mock_main.assert_called_once()
            
        finally:
            # Restaura a saída padrão
            sys.stdout = original_stdout


def test_main_keyboard_interrupt():
    """Testa a interrupção por teclado no módulo principal."""
    # Arrange
    with patch('src.interface.cli.cli_app.main') as mock_main:
        mock_main.side_effect = KeyboardInterrupt()
        
        # Redireciona a saída de erro padrão
        original_stderr = sys.stderr
        sys.stderr = StringIO()
        
        try:
            # Act
            with patch.object(sys, 'argv', ['main.py']):
                from main import main
                return_code = main()
                
            # Assert
            assert return_code == 0
            output = sys.stderr.getvalue()
            assert "Aplicação encerrada pelo usuário" in output
            
        finally:
            # Restaura a saída de erro padrão
            sys.stderr = original_stderr


def test_main_unexpected_error():
    """Testa o tratamento de erro inesperado no módulo principal."""
    # Arrange
    with patch('src.interface.cli.cli_app.main') as mock_main:
        mock_main.side_effect = Exception("Erro inesperado")
        
        # Redireciona a saída de erro padrão
        original_stderr = sys.stderr
        sys.stderr = StringIO()
        
        try:
            # Act
            with patch.object(sys, 'argv', ['main.py']):
                from main import main
                return_code = main()
                
            # Assert
            assert return_code == 1
            output = sys.stderr.getvalue()
            assert "Erro inesperado" in output
            
        finally:
            # Restaura a saída de erro padrão
            sys.stderr = original_stderr


def test_main_module_execution():
    """Testa a execução do módulo principal como um script."""
    # Arrange
    with patch('src.interface.cli.cli_app.main') as mock_main:
        mock_main.return_value = 0
        
        # Redireciona a saída padrão
        original_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # Act
            with patch.object(sys, 'argv', ['main.py']):
                import src.__main__  # Isso executará o código em __main__.py
                
            # Assert
            mock_main.assert_called_once()
            
        finally:
            # Restaura a saída padrão
            sys.stdout = original_stdout


def test_main_with_arguments():
    """Testa a execução do módulo principal com argumentos de linha de comando."""
    # Arrange
    with patch('src.interface.cli.cli_app.main') as mock_main:
        mock_main.return_value = 0
        
        # Redireciona a saída padrão
        original_stdout = sys.stdout
        sys.stdout = StringIO()
        
        test_args = ['main.py', '--debug', '--verbose']
        
        try:
            # Act
            with patch.object(sys, 'argv', test_args):
                from main import main
                return_code = main()
                
            # Assert
            assert return_code == 0
            mock_main.assert_called_once()
            
        finally:
            # Restaura a saída padrão
            sys.stdout = original_stdout
