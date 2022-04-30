FROM python:latest

WORKDIR /luxinity-ucp

COPY  . .

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./main.py" ]