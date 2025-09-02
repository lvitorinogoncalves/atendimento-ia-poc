"""Módulo que contém o adaptador para saída de voz."""
import pyttsx3
from typing import Optional, List, Dict, Any


class VoiceOutputError(Exception):
    """Exceção para erros de saída de voz."""
    pass


class VoiceOutputAdapter:
    """Adaptador para síntese de fala."""
    
    def __init__(self, rate: int = 150, volume: float = 0.9, voice_id: Optional[str] = None):
        """Inicializa o adaptador de saída de voz.
        
        Args:
            rate: Velocidade de fala em palavras por minuto.
            volume: Volume da fala (0.0 a 1.0).
            voice_id: ID da voz a ser utilizada. Se None, usa a voz padrão do sistema.
        """
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        
        # Configura a voz, se especificada
        if voice_id:
            self.set_voice(voice_id)
        else:
            # Tenta encontrar uma voz em português por padrão
            self._set_portuguese_voice()
    
    def _set_portuguese_voice(self):
        """Tenta configurar uma voz em português, se disponível."""
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'portuguese' in (voice.languages or []) or 'pt' in (voice.languages or []):
                self.engine.setProperty('voice', voice.id)
                return
        
        # Se não encontrar uma voz em português, usa a voz padrão
        if voices:
            self.engine.setProperty('voice', voices[0].id)
    
    def set_voice(self, voice_id: str) -> bool:
        """Define a voz a ser utilizada.
        
        Args:
            voice_id: ID da voz a ser utilizada.
            
        Returns:
            True se a voz foi definida com sucesso, False caso contrário.
        """
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if voice.id == voice_id:
                self.engine.setProperty('voice', voice_id)
                return True
        return False
    
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """Retorna uma lista de vozes disponíveis.
        
        Returns:
            Lista de dicionários com informações sobre as vozes disponíveis.
        """
        voices = self.engine.getProperty('voices')
        return [
            {
                'id': voice.id,
                'name': voice.name,
                'languages': voice.languages or [],
                'gender': voice.gender,
            }
            for voice in voices
        ]
    
    def speak(self, text: str) -> None:
        """Fala o texto fornecido.
        
        Args:
            text: Texto a ser falado.
            
        Raises:
            VoiceOutputError: Se ocorrer um erro ao tentar falar o texto.
        """
        try:
            print(f"IA: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            raise VoiceOutputError(f"Erro ao tentar falar o texto: {str(e)}")
    
    def __del__(self):
        """Libera recursos ao destruir o objeto."""
        try:
            self.engine.stop()
        except:
            pass
