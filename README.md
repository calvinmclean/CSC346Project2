# C46Project2

Database:
    host: csc346.cgt0vfrj0f4b.us-east-2.rds.amazonaws.com
    port: 3306
    username: csc346
    password: coridata

    to run sql files:
    mysql -h <host> -P 3306 -u csc346 -p < file.sql

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


TODO: notify after successfully adding corgi
TODO: remove contact entry when adding corgi since we are using owner's email?
