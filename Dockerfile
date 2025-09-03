FROM python:3.11.4

# Открываем порт для Streamlit


# Устанавливаем рабочую директорию
WORKDIR /app

# Обновляем систему и устанавливаем зависимости
# Используем buildkit + кешируемые слои
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    gnupg \
    curl \
    fonts-liberation \
    fontconfig \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    chromium-driver \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# Копируем кастомные .ttf-шрифты (папка рядом с Dockerfile)
COPY fonts/ /usr/share/fonts/truetype/custom/

# Обновляем кэш шрифтов
RUN fc-cache -f -v

# Кеш pip и requirements
ENV PIP_NO_CACHE_DIR=off
ENV PIP_CACHE_DIR=/root/.cache/pip

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем исходники приложения
COPY . .

# Переменные окружения для Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/lib/chromium/chromedriver
ENV PATH=$CHROMEDRIVER_PATH:$PATH

# Запуск приложения
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=80", "--server.address=0.0.0.0"]


