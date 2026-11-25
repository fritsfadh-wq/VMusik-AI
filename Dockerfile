FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r backend/requirements.txt

WORKDIR /app/backend

RUN python -c "import os; print('FILES:', os.listdir('.')); import main; print('IMPORT_OK')"

EXPOSE 3000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-3000}"]
