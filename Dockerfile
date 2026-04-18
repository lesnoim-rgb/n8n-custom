# Базовый образ n8n
FROM n8nio/n8n:latest

# Переключаемся на root для установки пакетов
USER root

# Обновляем пакеты и устанавливаем:
# - python3 и pip (для парсинга)
# - playwright (библиотеки для браузера)
# - wget, git (могут пригодиться)
RUN apk update && \
    apk add --no-cache \
        python3 \
        py3-pip \
        wget \
        git \
        chromium \
        chromium-chromedriver \
        freetype \
        harfbuzz \
        ca-certificates \
        ttf-freefont \
        nss \
        fontconfig

# Устанавливаем Python-библиотеки для парсинга
RUN pip3 install --no-cache-dir \
        playwright \
        beautifulsoup4 \
        requests \
        lxml \
        tenacity

# Устанавливаем Playwright браузеры
RUN playwright install chromium

# Устанавливаем кастомные ноды n8n (если нужны)
RUN cd /home/node/.n8n && \
    npm install @nikolaymatrosov/n8n-nodes-yandex360 \
                @bauer-group/n8n-nodes-http-throttled-request \
                n8n-nodes-supabase

# Возвращаемся к пользователю node (безопасность)
USER node

# Стандартные переменные n8n (Coolify их переопределит)
ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=5678
