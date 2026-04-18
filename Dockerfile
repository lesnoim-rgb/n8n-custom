FROM n8nio/n8n:latest

USER root

# Обновляем пакеты и устанавливаем зависимости (Debian/Ubuntu стиль)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        wget \
        git \
        chromium \
        chromium-driver \
        freetype2 \
        libharfbuzz0b \
        ca-certificates \
        fonts-freefont-ttf \
        libnss3 \
        fontconfig \
        libx11-xcb1 \
        libxcb1 \
        libxcomposite1 \
        libxcursor1 \
        libxdamage1 \
        libxi6 \
        libxtst6 \
        libxrandr2 \
        libasound2 \
        libatk-bridge2.0-0 \
        libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Python-библиотеки
RUN pip3 install --no-cache-dir \
    playwright \
    beautifulsoup4 \
    requests \
    lxml \
    tenacity

# Устанавливаем браузеры Playwright
RUN playwright install chromium

# Устанавливаем кастомные ноды n8n
RUN cd /home/node/.n8n && \
    npm install \
        @nikolaymatrosov/n8n-nodes-yandex360 \
        @bauer-group/n8n-nodes-http-throttled-request \
        n8n-nodes-supabase

USER node

ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=5678
