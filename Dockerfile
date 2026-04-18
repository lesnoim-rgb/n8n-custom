FROM node:18-alpine

# Устанавливаем n8n глобально
RUN npm config set python python3 && \
    npm install -g n8n

# Устанавливаем системные зависимости Alpine
RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    chromium \
    chromium-chromedriver \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    nss \
    fontconfig \
    && rm -rf /var/cache/apk/*

# Устанавливаем Python-библиотеки для парсинга
RUN pip3 install --no-cache-dir \
    playwright \
    beautifulsoup4 \
    requests \
    lxml \
    tenacity

# Устанавливаем браузеры Playwright
RUN playwright install chromium

# Создаём директорию для кастомных нод
RUN mkdir -p /home/node/.n8n && \
    cd /home/node/.n8n && \
    npm install \
        @nikolaymatrosov/n8n-nodes-yandex360 \
        @bauer-group/n8n-nodes-http-throttled-request \
        n8n-nodes-supabase

# Настройка окружения
ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=5678
ENV N8N_PATH=/home/node/.n8n

EXPOSE 5678

# Запуск n8n
CMD ["n8n", "start"]
