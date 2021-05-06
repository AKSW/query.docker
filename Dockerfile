FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY query.py .

ENTRYPOINT [ "python", "/usr/src/app/query.py" ]
