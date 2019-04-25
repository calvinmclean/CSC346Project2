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



### Project 03
New features:
- Github OAuth for login
- Github webhooks to automatically checkout new pushes or pull requests

New ec2 instance: http://ec2-3-86-254-204.compute-1.amazonaws.com

#### How to use webhook:
First you will need my fork of the repo since I needed permission to setup the webhook:

```shell
git clone https://github.com/calvinmclean/CSC346Project2.git
# or if you already have Laura's repo:
git remote add calvin https://github.com/calvinmclean/CSC346Project2.git
```

Demonstrate by:

1. making a small change on your local computer
    - I would edit `corgi_store/templates/home.html` and change the `<h1>` contents
2. commit and push:
```shell
git commit -am "edit title for webhook"
git push
# or if you added a remote:
git push calvin master
```
3. Wait about 5-10 seconds before refreshing the server page


#### How the webhook works
The program takes a personal access token from Github and creates a webhook. This webhook is configured to trigger on pushes and pull requests and will send a payload to http://ec2-3-86-254-204.compute-1.amazonaws.com:8000/webhook when one of these events occurs. This payload is a large JSON object containing all of the information about the repository and commit/PR.


On the server-side, a django endpoint is used to listen for the payload. This application has two important Python modules:
- PyGithub: used to authenticate with Github using the personal access token and create the webhook
- GitPython: used to perform all kinds of git operations including fetching, pulling, and cloning

The `webhook.py` file started by using [this example](https://pygithub.readthedocs.io/en/latest/examples/Webhook.html) and was modified to run inside Django and to add additional operations for interacting with git repositories.
