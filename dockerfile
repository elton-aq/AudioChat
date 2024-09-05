# Usar uma imagem base com Python
FROM python:3.10

# Instalar dependências do Python
RUN pip install --upgrade pip

# Instalar dependências do sistema, incluindo o portaudio para PyAudio
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    ffmpeg \
    libsm6 \
    libxext6 \
    cmake \
    rsync \
    libgl1-mesa-glx \
    python3-pyaudio \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0 \
    libasound-dev \
    --global-option='build_ext' --global-option='-I/usr/local/include' --global-option='-L/usr/local/lib' pyaudio \
    && rm -rf /var/lib/apt/lists/*

# Criar e definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto para o diretório de trabalho
COPY . /app

RUN pip install -r requirements.txt

# Exponha o segredo SECRET_EXAMPLE no momento da compilação e use seu valor como git remote URL 
RUN --mount= type =secret, id =API_KEY,mode=0444,required= true \
 git init && \
 git remoto adicionar origem $( cat /run/secrets/API_KEY)

# Comando para rodar o aplicativo
CMD ["python", "main.py"]