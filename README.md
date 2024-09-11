# AudioBot 

Um chatbot que utiliza LLM para conversação em tempo real

## Descrição

Este projeto é um chatbot por voz desenvolvido em Python que utiliza o modelo **LLaMA-70B** para gerar respostas inteligentes a partir de comandos de voz. O frontend é feito com Gradio, e o reconhecimento de voz é gerenciado pela biblioteca `speech_recognition`. Ele também utiliza Groq como API para acesso ao modelo.

## Instalação

### 1. Clonando o repositorio 
Clone o repositório:
```bash
git clone https://github.com/elton-aq/AudioChat.git
```

Entre no repositório:
```bash
cd AudioChat
```

### 2. Configuração de API Key

Para que o projeto funcione corretamente, é necessário obter uma **API_KEY** do serviço Groq e configurá-la no arquivo `.env`. Siga os passos abaixo:

1. Acesse [https://console.groq.com/keys](https://console.groq.com/keys) e faça login com sua conta.
2. No painel, gere uma nova chave de API.
3. Após gerar a chave, copie-a.
4. Crie um arquivo `.env` na raiz do projeto, se ainda não existir.
5. Dentro do arquivo `.env`, adicione a seguinte linha:
   ```bash
   API_KEY='insira_sua_chave_aqui'
   ```

Agora o projeto poderá acessar a API Groq usando a chave configurada.

### 3. Configurando o ambiente
Crie um ambiente virtual (opcional, mas recomendado): 
```bash
python -m venv venv
source venv/bin/activate  # ou 'venv\Scripts\activate' no Windows
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

## Modo de uso

Para começar a conversa, basta gravar o seu áudio. Assim que finalizar, o processamento será realizado automaticamente! Caso queira fazer outra pergunta, basta limpar o áudio anterior e gravar novamente. As respostas serão exibidas no chat, tanto em texto quanto faladas.

Execute o servidor localmente:
```bash
python main.py
```
