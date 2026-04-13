FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

WORKDIR /app

# Copiar requirements
COPY requirements.offline.txt .

# Instalar dependencias
RUN python -m venv ${VIRTUAL_ENV} && \
    pip install --no-cache-dir -r requirements.offline.txt

# Copiar código
COPY src/ src/

EXPOSE 8000

CMD ["uvicorn", "src.praetor.main:app", "--host", "0.0.0.0", "--port", "8000"]
