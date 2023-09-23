FROM python:3.10
WORKDIR /code/srv/
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY data_class.py data_class.py
COPY data_enums.py data_enums.py
COPY data_srv.py data_srv.py
WORKDIR /code/
CMD ["python", "-u", "-m", "srv.data_srv"]