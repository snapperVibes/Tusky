# Launches server (devolpment)
FROM python:3.8
WORKDIR /src

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Just eases devolpment
RUN echo 'alias py=python' >> ~/.bashrc

COPY . .

CMD ["python", "main.py"]
