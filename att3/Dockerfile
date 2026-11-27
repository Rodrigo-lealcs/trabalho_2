# Imagem base com Python
FROM python:3.12-slim

# Pasta de trabalho dentro do container
WORKDIR /app

# Instala as dependências primeiro (aproveita o cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto
COPY . .

# Mostra os prints e logs na hora, sem atraso
ENV PYTHONUNBUFFERED=1

# Porta em que a aplicação responde
EXPOSE 8000

# Comando que mantém a aplicação em execução
CMD ["python", "servidor.py"]
