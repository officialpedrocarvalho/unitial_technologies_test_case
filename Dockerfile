FROM python:3.9

WORKDIR /data_analyzer

COPY requirements.txt /data_analyzer/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /data_analyzer/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
