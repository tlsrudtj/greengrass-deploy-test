FROM python:3.10-slim
WORKDIR /app
RUN pip install paho-mqtt
COPY app.py .
CMD ["python", "app.py"]