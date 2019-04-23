# C46Project2


Django:
```shell
pip3 install django
sudo apt-get install python3-dev libmysqlclient-dev
pip3 install mysqlclient
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
python3 manage.py shell # to interact with REPL
```



```
docker build -t csc346 .
docker run --name csc346 -p 80:8000 -v `pwd`:/root -td csc346:latest runserver 0.0.0.0:8000
```


https://fosstack.com/how-to-add-google-authentication-in-django/
