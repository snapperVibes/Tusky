# Launches server (devolpment)
FROM python:3.8
WORKDIR /src

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
