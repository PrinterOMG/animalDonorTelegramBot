FROM python:3.11-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "bot.py"]
