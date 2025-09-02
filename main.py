#!/usr/bin/env python3
"""
Ponto de entrada principal para o sistema de atendimento por IA.

Este módulo inicia a aplicação de linha de comando para o sistema de atendimento por IA,
que permite interagir com um assistente virtual por voz ou texto.
"""
import sys
from src.interface.cli.cli_app import main as cli_main


def main():
    """Função principal que inicia a aplicação."""
    try:
        # Inicia a aplicação CLI
        sys.exit(cli_main())
    except KeyboardInterrupt:
        print("\nAplicação encerrada pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
