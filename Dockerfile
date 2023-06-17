FROM python:3.11.3-slim
LABEL authors="Nikolay Sysoev"
COPY requirements.txt /opt/devman_bot/requirements.txt
WORKDIR /opt/devman_bot
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["python", "run_check_lessons.py"]
