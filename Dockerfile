FROM python:3.11.3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN command pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]

