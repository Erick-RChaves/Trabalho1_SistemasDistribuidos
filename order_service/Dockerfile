FROM python:3.9-slim #Imagem base do Python leve

WORKDIR /app   #Define diretório de trabalho dentro do container

COPY requirimentes.txt . #Copia as dependências
RUN pip install --no-cache-dir -r requirements.txt

COPY . . # Copia o código fonte para o container

# Portas expostas são definidas no docker-compose, não aqui
