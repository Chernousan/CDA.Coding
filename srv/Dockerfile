FROM python:latest
WORKDIR /code
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY dataClass.py dataClass.py
COPY dataEnums.py dataEnums.py
COPY srv.py srv.py
CMD ["python", "-u", "srv.py"]