FROM python:3.12

RUN apt update 
RUN pip install requests \
pydantic==2.8.2 \
pydantic-settings==2.3.4 \
fastapi \
matplotlib \
numpy \
uvicorn[standard] 

WORKDIR /app
COPY . .
ENV PYTHONDONTWRITEBYTECODE=1
ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
