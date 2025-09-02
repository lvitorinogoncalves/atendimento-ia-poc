"""Módulo que contém a interface de linha de comando da aplicação."""
import sys
import time
from typing import List, Optional

from ...domain.entities.message import Message, MessageRole
from ...domain.use_cases.process_message import ProcessMessageUseCase, ProcessMessageInput
from ...infrastructure.adapters.smart_ai_adapter import SmartAIModel
from ...infrastructure.adapters.direct_ollama_adapter import DirectOllamaModel
from ...infrastructure.adapters.voice_input import VoiceInputAdapter
from ...infrastructure.adapters.voice_output import VoiceOutputAdapter
from ...infrastructure.config.settings import settings


class CLIApp:
    """Classe principal da aplicação de linha de comando."""
    
    def __init__(self):
        """Inicializa a aplicação com as dependências necessárias."""
        # Inicializa o modelo de IA baseado na configuração
        if settings.OLLAMA_ENABLED:
            print("🦙 Usando Ollama diretamente...")
            self.ai_model = DirectOllamaModel(
                model_name=settings.OLLAMA_MODEL,
                base_url=settings.OLLAMA_BASE_URL
            )
        else:
            print("🤖 Usando sistema de fallback inteligente...")
            self.ai_model = SmartAIModel(
                openai_api_key=settings.OPENAI_API_KEY,
                deepseek_api_key=settings.DEEPSEEK_API_KEY
            )
        
        # Inicializa o caso de uso
        self.process_message_use_case = ProcessMessageUseCase(ai_model=self.ai_model)
        
        # Inicializa os adaptadores de entrada/saída de voz
        self.voice_input = VoiceInputAdapter(
            language=settings.VOICE_LANGUAGE,
            energy_threshold=settings.SPEECH_ENERGY_THRESHOLD,
            pause_threshold=settings.SPEECH_PAUSE_THRESHOLD
        )
        
        self.voice_output = VoiceOutputAdapter(
            rate=settings.VOICE_RATE,
            volume=settings.VOICE_VOLUME
        )
        
        # Histórico da conversa
        self.conversation_history: List[Message] = []
    
    def print_banner(self) -> None:
        """Exibe o banner de boas-vindas da aplicação."""
        banner = f"""
        ╔══════════════════════════════════════╗
        ║                                      ║
        ║   {settings.APP_NAME} v{settings.APP_VERSION}   ║
        ║   Assistente de Atendimento por Voz   ║
        ║                                      ║
        ╚══════════════════════════════════════╝
        """
        print(banner)
    
    def print_help(self) -> None:
        """Exibe as instruções de uso."""
        help_text = """
        Comandos disponíveis:
        - fale: Iniciar o modo de fala
        - texto: Digitar uma mensagem
        - historico: Ver histórico da conversa
        - limpar: Limpar o histórico da conversa
        - ajuda: Mostrar esta ajuda
        - sair: Encerrar o atendimento
        """
        print(help_text)
    
    def listen_for_command(self) -> str:
        """Aguarda e retorna um comando do usuário."""
        try:
            return input("\nDigite um comando (ou 'ajuda' para ver os comandos): ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            return "sair"
    
    def process_text_command(self) -> Optional[str]:
        """Processa um comando de texto digitado pelo usuário."""
        try:
            text = input("Digite sua mensagem: ").strip()
            if not text:
                print("Mensagem vazia. Tente novamente.")
                return None
            return text
        except (KeyboardInterrupt, EOFError):
            return None
    
    def process_voice_command(self) -> Optional[str]:
        """Processa um comando de voz do usuário."""
        print("Ouvindo... (pressione Ctrl+C para cancelar)")
        try:
            success, text = self.voice_input.listen()
            if not success:
                print(f"Erro: {text}")
                return None
            return text
        except KeyboardInterrupt:
            print("\nCaptura de voz cancelada pelo usuário.")
            return None
        except Exception as e:
            print(f"Erro ao processar comando de voz: {str(e)}")
            return None
    
    def show_conversation_history(self) -> None:
        """Exibe o histórico da conversa."""
        if not self.conversation_history:
            print("Nenhuma mensagem no histórico.")
            return
            
        print("\n=== Histórico da Conversa ===")
        for i, msg in enumerate(self.conversation_history, 1):
            role = "Você" if msg.role == MessageRole.USER else "IA"
            print(f"{i}. [{role}] {msg.content}")
        print("===========================\n")
    
    def clear_conversation_history(self) -> None:
        """Limpa o histórico da conversa."""
        self.conversation_history.clear()
        print("Histórico da conversa limpo com sucesso!")
    
    def process_user_message(self, user_message: str) -> None:
        """Processa uma mensagem do usuário e obtém uma resposta da IA."""
        if not user_message:
            return
            
        # Prepara a entrada para o caso de uso
        input_data = ProcessMessageInput(
            user_message=user_message,
            conversation_history=self.conversation_history,
            model_kwargs={
                "max_tokens": settings.OPENAI_MAX_TOKENS,
                "temperature": settings.OPENAI_TEMPERATURE
            }
        )
        
        try:
            # Executa o caso de uso
            output = self.process_message_use_case.execute(input_data)
            
            # Adiciona as mensagens ao histórico
            self.conversation_history.append(output.user_message)
            self.conversation_history.append(output.assistant_message)
            
            # Fala a resposta
            self.voice_output.speak(output.response)
            
        except Exception as e:
            error_msg = f"Desculpe, ocorreu um erro ao processar sua mensagem: {str(e)}"
            print(f"Erro: {error_msg}")
            self.voice_output.speak("Desculpe, ocorreu um erro ao processar sua mensagem.")
    
    def run(self) -> None:
        """Executa o loop principal da aplicação."""
        self.print_banner()
        self.voice_output.speak("Bem-vindo ao assistente de atendimento por voz. Como posso ajudar?")
        
        while True:
            try:
                command = self.listen_for_command()
                
                if command == "sair" or command == "exit" or command == "quit":
                    self.voice_output.speak("Obrigado por utilizar nosso atendimento. Até mais!")
                    print("Atendimento encerrado.")
                    break
                    
                elif command == "ajuda" or command == "help" or command == "?":
                    self.print_help()
                    
                elif command == "fale" or command == "voz" or command == "voice":
                    user_message = self.process_voice_command()
                    if user_message:
                        self.process_user_message(user_message)
                        
                elif command == "texto" or command == "digitar" or command == "text":
                    user_message = self.process_text_command()
                    if user_message:
                        self.process_user_message(user_message)
                        
                elif command == "historico" or command == "history":
                    self.show_conversation_history()
                    
                elif command == "limpar" or command == "clear" or command == "limpar historico":
                    self.clear_conversation_history()
                    
                elif command:
                    print(f"Comando não reconhecido: {command}")
                    print("Digite 'ajuda' para ver os comandos disponíveis.")
                
            except KeyboardInterrupt:
                print("\nAtendimento interrompido pelo usuário.")
                self.voice_output.speak("Atendimento interrompido.")
                break
                
            except Exception as e:
                print(f"\nErro inesperado: {str(e)}")
                if settings.DEBUG:
                    import traceback
                    traceback.print_exc()
                self.voice_output.speak("Desculpe, ocorreu um erro inesperado.")


def main():
    """Função principal para iniciar a aplicação."""
    try:
        app = CLIApp()
        app.run()
    except Exception as e:
        print(f"Erro ao iniciar a aplicação: {str(e)}")
        if settings.DEBUG:
            import traceback
            traceback.print_exc()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
