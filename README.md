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


Currently hosted at:

http://ec2-107-22-60-201.compute-1.amazonaws.com/

and

http://ec2-184-72-79-174.compute-1.amazonaws.com/

Load balancer:

http://csc346-corgi-store-1777772867.us-east-1.elb.amazonaws.com/


TODO: notify after successfully adding corgi
TODO: remove contact entry when adding corgi since we are using owner's email?

docker build -t csc346 .
docker run --name csc346 -p 80:8000 -td csc346:latest runserver 0.0.0.0:8000
