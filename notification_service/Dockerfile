# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Comando será especificado no docker-compose.yml, mas expomos as portas
# EXPOSE 50051
# EXPOSE 50052
# Portas expostas são definidas no docker-compose, não aqui

