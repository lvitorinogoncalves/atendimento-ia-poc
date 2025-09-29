# Atendimento por Voz com IA

Sistema de atendimento por voz que utiliza **múltiplos modelos de IA** para responder perguntas em tempo real, desenvolvido seguindo os princípios de **Clean Architecture** e **Clean Code**.

## 🚀 Funcionalidades

* 🎙️ **Reconhecimento de voz em português**
* 🤖 **Integração Multi-Model AI**

  * **OpenAI GPT-3.5-turbo** (primário)
  * **DeepSeek** (fallback secundário)
  * **Ollama** (modelos locais como backup final)
* 🔄 **Fallback inteligente com failover transparente**

  * Detecção automática de erros de *quota* e *rate limiting*
  * Alternância automática entre modelos sem interromper o atendimento
* 💬 Interface de **linha de comando interativa**
* 📜 **Histórico de conversas** para manter contexto
* ⚙️ **Configurações flexíveis** via `.env`
* 🛠️ **Arquitetura limpa, modular e resiliente**
* 🧪 Suporte a **testes automatizados** com `pytest`

## 📋 Pré-requisitos

* Python 3.8 ou superior
* Microfone e alto-falantes
* Conta na **OpenAI** (obrigatória)
* Conta na **DeepSeek** (opcional, usada no fallback)
* **Ollama** instalado para uso de modelos locais
* Git (opcional, apenas para clonar o repositório)

## 🛠️ Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/atendimento-ia-poc.git
   cd atendimento-ia-poc
   ```

2. Crie e ative um ambiente virtual:

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
   # OpenAI (obrigatório)
   OPENAI_API_KEY=sua_chave_aqui
   OPENAI_MODEL=gpt-3.5-turbo
   OPENAI_MAX_TOKENS=150
   OPENAI_TEMPERATURE=0.7

   # DeepSeek (opcional, usado no fallback)
   DEEPSEEK_API_KEY=sua_chave_aqui

   # Configurações de voz
   VOICE_RATE=150
   VOICE_VOLUME=0.9
   VOICE_LANGUAGE=pt-BR

   # Reconhecimento de fala
   SPEECH_ENERGY_THRESHOLD=300
   SPEECH_PAUSE_THRESHOLD=0.8

   # Configurações gerais
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

   * `fale`: Iniciar o modo de fala
   * `texto`: Digitar uma mensagem
   * `historico`: Ver histórico da conversa
   * `limpar`: Limpar o histórico da conversa
   * `ajuda`: Mostrar ajuda
   * `sair`: Encerrar o atendimento

3. Fale claramente quando solicitado ou digite sua mensagem.

## 🏗️ Estrutura do Projeto

```
src/
├── domain/                  # Lógica de domínio
│   ├── entities/            # Entidades de domínio
│   └── use_cases/           # Casos de uso
├── infrastructure/          # Implementações concretas
│   ├── adapters/            # Adaptadores para serviços externos (OpenAI, DeepSeek, Ollama)
│   └── config/              # Configurações
└── interface/               # Interfaces de usuário
    └── cli/                 # Interface de linha de comando

tests/                      # Testes automatizados
├── unit/                   # Testes unitários
└── integration/            # Testes de integração
```

## ✅ Suporte ao Ollama

Este projeto já conta com integração ao **Ollama** como última camada de fallback.

### Testando o Ollama:

```powershell
ollama list
ollama pull llama2
ollama run llama2 "Olá, como você está?"
```

---

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

Contribuições são bem-vindas! Abra uma issue ou envie um pull request.

## 📞 Suporte

Para suporte, por favor abra uma issue no repositório.
