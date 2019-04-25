from __future__ import print_function

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from github import Github
from vars import *
import git, os, subprocess

ENDPOINT = "webhook"

@view_defaults(
    route_name=ENDPOINT, renderer="json", request_method="POST"
)
class PayloadView(object):
    """
    View receiving of Github payload. By default, this view it's fired only if
    the request is json and method POST.
    """

    def __init__(self, request):
        self.payload = request.json
        self.repo_name = self.payload['repository']['name']
        self.repo_dir = '{}/{}'.format(BASE_DIR, self.repo_name)
        self.clone_url = self.payload['repository']['clone_url']
        self.repo = git.Repo(self.repo_dir) \
            if os.path.isdir(self.repo_dir) and os.path.exists(self.repo_dir) \
            else git.Repo.clone_from(clone_url, self.repo_dir)

    @view_config(header="X-Github-Event:push")
    def payload_push(self):
        """This method is a continuation of PayloadView process, triggered if
        header HTTP-X-Github-Event type is Push"""
        print("No. commits in push:", len(self.payload['commits']))
        self.checkout_push()
        return Response("success")

    def checkout_push(self):
        # Checkout master first
        [head for head in self.repo.heads if head.name == "master"][0].checkout()
        # Checkout branch that commit is attached to
        ref = self.payload['ref']
        if ref == "refs/heads/{}".format(self.repo.active_branch.name):
            self.repo.git.pull()
        else:
            print("Checking out ref {}".format(ref))
            self.repo.remotes[0].fetch("{}:{}".format(ref, ref.split('/')[-1]))
            [head for head in self.repo.heads if head.name == ref.split('/')[-1]][0].checkout()
            # Checkout commit
            commit = self.payload['head_commit']['id']
            print("Checking out latest commit {}".format(commit))
            self.repo.git.checkout(commit)

    @view_config(header="X-Github-Event:pull_request")
    def payload_pull_request(self):
        """This method is a continuation of PayloadView process, triggered if
        header HTTP-X-Github-Event type is Pull Request"""
        print("PR number", self.payload['pull_request']['number'], self.payload['action'])
        print("PR title:", self.payload['pull_request']['title'])
        print("No. Commits in PR:", self.payload['pull_request']['commits'])
        # Checkout PR if it is newly opened or reopened
        if 'open' in self.payload['action']:
            self.checkout_pr()
            os.chdir("{}/{}".format(BASE_DIR, self.repo_name))
            # subprocess.run(['docker-compose', 'build'])
            # subprocess.run(['docker-compose', 'up', '-d'])
        return Response("success")

    def checkout_pr(self):
        # Checkout master first
        [head for head in self.repo.heads if head.name == "master"][0].checkout()
        print("Checking out new PR")
        number = self.payload['pull_request']['number']
        self.repo.remotes[0].fetch('pull/{}/head:pull_{}'.format(number, number))
        print("Fetched PR #{} and created branch 'pull_{}'".format(number, number))
        [head for head in self.repo.heads if head.name == "pull_{}".format(number)][0].checkout()
        print("Checked out PR #{} on branch 'pull_{}'".format(number, number))

    @view_config(header="X-Github-Event:ping")
    def payload_else(self):
        print("Pinged! Webhook created with id {}!".format(self.payload["hook"]["id"]))
        return {"status": 200}


def create_webhook(repo_name):
    """ Creates a webhook for the specified repository.

    This is a programmatic approach to creating webhooks with PyGithub's API. If you wish, this can be done
    manually at your repository's page on Github in the "Settings" section. There is a option there to work with
    and configure Webhooks.
    """

    config = {
        "url": "http://{host}/{endpoint}".format(host=HOST, endpoint=ENDPOINT),
        "content_type": "json"
    }

    g = Github(PERSONAL_ACCESS_TOKEN)
    repo = g.get_repo("{}/{}".format(OWNER, repo_name))
    repo.create_hook("web", config, EVENTS, active=True)
    # Clone repo if DNE
    repo_dir = "{}/{}".format(BASE_DIR, repo_name)
    if not (os.path.isdir(repo_dir) and os.path.exists(repo_dir)):
        git.Repo.clone_from(repo.clone_url, repo_dir)


def main():
    config = Configurator()
    for repo in REPOS:
        create_webhook(repo)

    config.add_route(ENDPOINT, "/{}".format(ENDPOINT))
    config.scan()

    app = config.make_wsgi_app()
    server = make_server("0.0.0.0", 8080, app)
    server.serve_forever()


if __name__ == "__main__":
    main()
