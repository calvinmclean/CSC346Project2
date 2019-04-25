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
- Github webhooks to automatically checkout new pushes
- Run using Docker. The Dockerfile in this project uses the official Python Docker image and installs our dependencies in it so it can easily be run in any cloud environment

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
3. Wait about 5-10 seconds before refreshing the browser page


#### How the webhook works
On Github, I was able to create a webhook for this repository that will trigger whenever new code is pushed to the repository. This webhook will send a payload to http://ec2-3-86-254-204.compute-1.amazonaws.com/webhook/ whenever this event occurs. This payload is a large JSON object containing all of the information about the repository and commit that was pushed.


On the server-side, a django endpoint is used to listen for the payload. This uses an important Python module:
- GitPython: used to perform all kinds of git operations including fetching, pulling, and cloning


This webhook is employed to enable a popular development technique that is enabled by cloud technologies: Continuous Integration or Continuous Development (CI/CD). The purpose of this is to automate the process of deploying new code to servers in testing or production environments. It allows developers to make changes to code without worrying about manually installing and testing their code on a cloud instance. CI/CD can be used to automatically run unit tests on pull requests, then merge the changes into master branch after the tests pass, and automatically deploy any changes on the master branch to the production servers.


The webhook code started by using [this example](https://pygithub.readthedocs.io/en/latest/examples/Webhook.html) and was modified to run inside Django. I only implemented the webhook for pushes since it is easier to demonstrate than pull requests, but the same can easily be done for a pull request.
