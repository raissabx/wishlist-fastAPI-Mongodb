# Use uma imagem base do Python
FROM python:3.11.4

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos de dependências para o contêiner
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos da aplicação para o contêiner
COPY . .

# Expõe a porta em que a aplicação estará em execução
# EXPOSE 8000

# Comando para iniciar a aplicação quando o contêiner for iniciado
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
