FROM ubuntu:20.4
FROM python:3.11.3
LABEL authors="Nikolay Sysoev"
WORKDIR /opt/devman_bot
COPY . .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
CMD ["python", "run_check_lessons.py"]
