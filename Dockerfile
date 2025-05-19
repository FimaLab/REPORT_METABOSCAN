FROM python:3.10.9

# Открываем порт для Streamlit
EXPOSE 8501

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости ОС
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    curl \
    fonts-liberation \
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

# Устанавливаем Python-зависимости
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Задаём переменные окружения, чтобы selenium нашёл chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/lib/chromium/chromedriver
ENV PATH=$CHROMEDRIVER_PATH:$PATH

# Запуск Streamlit
CMD ["streamlit", "run", "streamlit_app.py"]
