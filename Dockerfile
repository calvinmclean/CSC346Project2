FROM python
RUN pip install django mysqlclient
EXPOSE 8000
ADD . .
ENTRYPOINT ["python", "manage.py", "runserver"]
