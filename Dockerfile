# Используем базовый образ Nginx + Python
FROM nginx:latest

# Устанавливаем Python
RUN apt update && apt install -y python3 python3-pip gunicorn

# Устанавливаем Flask (или FastAPI, Django)
RUN pip3 install flask gunicorn

# Копируем файлы приложения
COPY app /app
COPY nginx.conf /etc/nginx/nginx.conf

# Запускаем Gunicorn и Nginx
CMD service nginx start && gunicorn -w 4 -b 0.0.0.0:8080 app:app