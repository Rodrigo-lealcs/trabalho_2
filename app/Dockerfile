# Imagem base enxuta com Python
FROM python:3.12-slim

WORKDIR /app

# Dependências primeiro: o Docker reaproveita essa camada se o requirements.txt não mudar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Usuário sem privilégios: se o serviço for invadido, o atacante não é root no container
RUN useradd --create-home --uid 1000 app && mkdir -p /app/data && chown -R app:app /app
COPY --chown=app:app . .
USER app

ENV PYTHONUNBUFFERED=1 DADOS_DIR=/app/data PORTA=8000
EXPOSE 8000

# O Docker marca o container como "unhealthy" se /saude parar de responder
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request,os; urllib.request.urlopen('http://127.0.0.1:'+os.environ['PORTA']+'/saude', timeout=3)"

# Cria os dados de exemplo só na primeira vez (não sobrescreve) e sobe o serviço
CMD ["sh", "-c", "python dados_exemplo.py && exec python servidor.py"]
