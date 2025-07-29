FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install .
VOLUME ["/app/data"]
CMD ["python", "-m", "dkenergy", "--full"]
