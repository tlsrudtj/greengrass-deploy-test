FROM python:3.10-slim
WORKDIR /app
RUN pip install pymongo[srv]
COPY app.py .
CMD ["python", "app.py"]