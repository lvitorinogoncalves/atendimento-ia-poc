import os
import time
import speech_recognition as sr
import pyttsx3
from openai import OpenAI
from dotenv import load_dotenv

# Configurações iniciais
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Inicializa o reconhecedor de fala
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Inicializa o sintetizador de fala
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Configura a voz em português (se disponível)
for voice in voices:
    if 'portuguese' in voice.languages or 'pt' in voice.languages:
        engine.setProperty('voice', voice.id)
        break

def falar(texto):
    """Faz o computador falar o texto"""
    print(f"IA: {texto}")
    engine.say(texto)
    engine.runAndWait()

def ouvir():
    """Ouve o áudio do microfone e converte para texto"""
    with microphone as source:
        print("\nFale agora...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
        try:
            texto = recognizer.recognize_google(audio, language='pt-BR')
            print(f"Você: {texto}")
            return texto
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"Erro ao acessar o serviço de reconhecimento de fala: {e}")
            return ""

def obter_resposta_ia(mensagem, historico=[]):
    """Obtém uma resposta da API da OpenAI"""
    try:
        # Prepara o histórico de mensagens
        mensagens = [
            {"role": "system", "content": "Você é um assistente virtual de atendimento telefônico. Seja prestativo e objetivo."}
        ]
        
        # Adiciona o histórico da conversa
        for msg in historico[-4:]:  # Mantém apenas as últimas 4 mensagens para contexto
            mensagens.append(msg)
            
        # Adiciona a mensagem atual
        mensagens.append({"role": "user", "content": mensagem})
        
        # Chama a API
        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=mensagens,
            max_tokens=150
        )
        
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro ao chamar a API: {e}")
        return "Desculpe, estou com dificuldades para responder no momento."

def main():
    print("=== Atendimento por Voz com IA ===")
    print("Diga 'tchau' para encerrar o atendimento.")
    
    historico = []
    falar("Olá! Como posso te ajudar hoje?")
    
    while True:
        # Ouve o usuário
        mensagem = ouvir().lower()
        
        # Verifica se quer encerrar
        if not mensagem or 'tchau' in mensagem or 'adeus' in mensagem:
            falar("Obrigado por entrar em contato. Tenha um ótimo dia!")
            break
            
        # Obtém a resposta da IA
        resposta = obter_resposta_ia(mensagem, historico)
        
        # Atualiza o histórico
        historico.append({"role": "user", "content": mensagem})
        historico.append({"role": "assistant", "content": resposta})
        
        # Fala a resposta
        falar(resposta)

if __name__ == "__main__":
    main()
