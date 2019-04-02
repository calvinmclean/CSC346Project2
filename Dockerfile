FROM python
RUN pip install django mysqlclient
EXPOSE 8000
WORKDIR /root
ENTRYPOINT ["python", "manage.py"]
