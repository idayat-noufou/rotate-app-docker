# Installation des dépendances
FROM python:3.11-alpine AS build

ARG APP_HOME=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR $APP_HOME

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt .
RUN python -m venv venv \
    && . venv/bin/activate \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copie uniquement du nécessaire
FROM python:3.11-alpine

ARG APP_HOME=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="$APP_HOME/venv/bin:$PATH"

WORKDIR $APP_HOME

RUN apk add --no-cache libffi

COPY --from=build $APP_HOME /app
COPY . .

EXPOSE 5000

LABEL maintainer="idayat.noufou@ynov.com" \
      version="1.0" \
      description="TP docker rotate-app-docker"

CMD ["python", "app.py"]
