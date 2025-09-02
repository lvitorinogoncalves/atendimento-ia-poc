"""Módulo que contém o adaptador para entrada de voz."""
import speech_recognition as sr
from typing import Optional, Tuple


class VoiceInputError(Exception):
    """Exceção para erros de entrada de voz."""
    pass


class VoiceInputAdapter:
    """Adaptador para captura de áudio do microfone e reconhecimento de fala."""
    
    def __init__(self, language: str = 'pt-BR', energy_threshold: int = 300, pause_threshold: float = 0.8):
        """Inicializa o adaptador de entrada de voz.
        
        Args:
            language: Idioma para reconhecimento de fala (padrão: 'pt-BR').
            energy_threshold: Limiar de energia para detecção de fala.
            pause_threshold: Tempo de pausa (em segundos) para considerar o fim da fala.
        """
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.language = language
        
        # Configura os parâmetros do reconhecedor
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.pause_threshold = pause_threshold
        
        # Ajusta para o ruído ambiente
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    def listen(self) -> Tuple[bool, str]:
        """Ouve o áudio do microfone e converte para texto.
        
        Returns:
            Uma tupla contendo um booleano indicando sucesso e o texto reconhecido.
            Em caso de falha, o texto contém a mensagem de erro.
        """
        try:
            with self.microphone as source:
                print("\nOuvindo... (fale agora)")
                audio = self.recognizer.listen(source)
                
            print("Processando áudio...")
            text = self.recognizer.recognize_google(audio, language=self.language)
            print(f"Você disse: {text}")
            return True, text
            
        except sr.UnknownValueError:
            return False, "Não foi possível entender o áudio"
            
        except sr.RequestError as e:
            error_msg = f"Erro ao acessar o serviço de reconhecimento de fala: {e}"
            print(error_msg)
            return False, error_msg
            
        except Exception as e:
            error_msg = f"Erro inesperado ao processar áudio: {str(e)}"
            print(error_msg)
            return False, error_msg
