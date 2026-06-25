FROM python:3.11-slim

WORKDIR /app

# Системные зависимости для Chromium (без ttf-unifont и ttf-ubuntu-font-family
# — они недоступны на Debian Trixie и не нужны для рендера карточек)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    fonts-liberation \
    wget \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем только Chromium, без --with-deps (deps уже выше)
RUN playwright install chromium

COPY . .

CMD ["python", "server.py"]
