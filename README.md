# Atendimento por Voz com IA

Sistema de atendimento por voz que utiliza IA para responder perguntas em tempo real, desenvolvido seguindo os princípios de Clean Architecture e Clean Code.

## 🚀 Funcionalidades

- 🎙️ Reconhecimento de voz em português
- 🤖 Respostas em tempo real usando a API da OpenAI (GPT-3.5-turbo)
- 💬 Interface de linha de comando interativa
- 📜 Histórico de conversa
- ⚙️ Configurações personalizáveis
- 🛠️ Arquitetura limpa e modular
- 🧪 Pronto para testes

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Microfone funcional
- Alto-falantes
- Conta na OpenAI (para obter uma chave de API)
- Git (opcional, apenas para clonar o repositório)

## 🛠️ Instalação

1. Clone o repositório (ou baixe o código fonte):
   ```bash
   git clone https://github.com/seu-usuario/atendimento-ia-poc.git
   cd atendimento-ia-poc
   ```

2. Crie e ative um ambiente virtual (recomendado):
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
   ```env
   # Chave da API da OpenAI (obrigatória)
   OPENAI_API_KEY=sua_chave_aqui
   
   # Configurações opcionais (valores padrão mostrados)
   OPENAI_MODEL=gpt-3.5-turbo
   OPENAI_MAX_TOKENS=150
   OPENAI_TEMPERATURE=0.7
   
   # Configurações de voz
   VOICE_RATE=150
   VOICE_VOLUME=0.9
   VOICE_LANGUAGE=pt-BR
   
   # Configurações de reconhecimento de fala
   SPEECH_ENERGY_THRESHOLD=300
   SPEECH_PAUSE_THRESHOLD=0.8
   
   # Configurações da aplicação
   APP_NAME=Atendimento IA
   APP_VERSION=0.1.0
   DEBUG=False
   ```

## 🚀 Como Usar

1. Inicie o aplicativo:
   ```bash
   python main.py
   ```

2. Comandos disponíveis:
   - `fale`: Iniciar o modo de fala
   - `texto`: Digitar uma mensagem
   - `historico`: Ver histórico da conversa
   - `limpar`: Limpar o histórico da conversa
   - `ajuda`: Mostrar ajuda
   - `sair`: Encerrar o atendimento

3. Fale claramente quando solicitado ou digite sua mensagem.

## 🏗️ Estrutura do Projeto

```
src/
├── domain/                  # Lógica de domínio
│   ├── entities/            # Entidades de domínio
│   └── use_cases/           # Casos de uso
├── infrastructure/          # Implementações concretas
│   ├── adapters/            # Adaptadores para serviços externos
│   └── config/              # Configurações
└── interface/               # Interfaces de usuário
    └── cli/                 # Interface de linha de comando

tests/                      # Testes automatizados
├── unit/                   # Testes unitários
└── integration/            # Testes de integração
```

## 🧪 Testes

Para executar os testes:

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Executar testes
pytest
```

## 📝 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.

## 📞 Suporte

Para suporte, por favor abra uma issue no repositório.

---

Desenvolvido com ❤️ por [Seu Nome]

## ✅ **Status: Ollama já está rodando!**

### **1. Verificar se está funcionando:**
```powershell
ollama list
```

### **2. Baixar o modelo (em outro terminal):**
```powershell
ollama pull llama2
```

### **3. Testar o modelo:**
```powershell
ollama run llama2 "Olá, como você está?"
```

## 🚀 **Agora vamos implementar o adaptador Ollama no sistema:**

### **1. Primeiro, vamos criar o adaptador Ollama:**
