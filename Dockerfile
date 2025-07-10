FROM registry.vsfi.ru/library/python:3.12-slim as builder

RUN apt-get update && apt-get install -y build-essential
COPY requirements.txt requirements.txt
RUN pip wheel --index-url https://nexus.vsfi.ru/repository/pypi/simple/ --wheel-dir /wheels -r requirements.txt

FROM registry.vsfi.ru/library/python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


WORKDIR /app
COPY --from=builder /wheels /wheels
COPY requirements.txt requirements.txt
RUN pip install --index-url https://nexus.vsfi.ru/repository/pypi/simple/ --find-links=/wheels -r requirements.txt 
COPY . .

ENTRYPOINT ["python", "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
