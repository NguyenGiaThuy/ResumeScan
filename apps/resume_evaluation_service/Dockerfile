FROM python:3.12-alpine

WORKDIR /graph

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p graph_diagrams

EXPOSE 8000

CMD ["python3", "main.py", "--minio"]
