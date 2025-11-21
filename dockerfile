# Использовал UV что бы не ждать долго сборки и пока зависимости поднянутся, решил не убирать(Ну а так опционально)
FROM python:3.11.9

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY requirements.txt .

RUN uv pip install --system -r requirements.txt 

COPY . .

EXPOSE 8080

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8080"]