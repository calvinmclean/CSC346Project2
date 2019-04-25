FROM python
RUN pip install django mysqlclient social-auth-app-django gitpython
EXPOSE 8000
WORKDIR /root
ENTRYPOINT ["python", "manage.py"]
