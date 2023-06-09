FROM python:3.10.7
WORKDIR /tmp
COPY ./requirements.txt /tmp/
# RUN pip install -r /tmp/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8888
# CMD ["manage.py", "runserver", "0.0.0.0:8000"]
