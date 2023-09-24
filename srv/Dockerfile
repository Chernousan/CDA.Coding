FROM python:3.10
WORKDIR /code/srv/
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app.py app.py
COPY data.py data.py
COPY enums.py enums.py
COPY helpers.py helpers.py
COPY http_srv.py http_srv.py
COPY spider.py spider.py
COPY pipeline.py pipeline.py
WORKDIR /code/
CMD ["python", "-u", "-m", "srv.app"]