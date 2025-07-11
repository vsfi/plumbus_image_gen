FROM registry.vsfi.ru/library/python:3.12-bookworm as builder
RUN printf "deb [trusted=yes] https://nexus.vsfi.ru/repository/debian-12/ bookworm main non-free-firmware\ndeb [trusted=yes] https://nexus.vsfi.ru/repository/debian-12/ bookworm-updates main non-free-firmware\ndeb [trusted=yes] https://nexus.vsfi.ru/repository/debian-12-security/ bookworm-security main\ndeb [trusted=yes] https://nexus.vsfi.ru/repository/apt-docker/ bookworm stable\n" > /etc/apt/sources.list
RUN printf "machine nexus.vsfi.ru\nlogin debian\npassword debian\n" > /etc/apt/auth.conf && echo "" > /etc/apt/sources.list.d/debian.sources

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
