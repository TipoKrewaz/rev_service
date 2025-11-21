# Сервис назначения ревьюеров на Python FastAPi
Всем привет кто это читает, в каждом файлике постарался написать комментарий(что бы объяснить логику своих действий)
Все зависимости представлены в - reqquirements.txt

# Локальная разработка с uv

Установите [uv](https://docs.astral.sh/uv/): curl -LsSf https://astral.sh/uv/install.sh | sh
Далее: 
source .venv/bin/activate
alembic upgrade head
uvicorn app.main:app --reload