#!/usr/bin/env python3
#
# usage:
# python3 .travis/push_readme.py org/repo README.md

import json
import os
import sys

from http.client import HTTPSConnection

def login(repo, username, password):
    """
    Sign into the dockerhub web UI and return JWT token.
    """

    url = "https://hub.docker.com/v2/users/login/"
    headers = { "Content-Type": "application/json" }
    body = { "username": username, "password": password }

    client = HTTPSConnection("hub.docker.com")
    client.request("POST", url, body=json.dumps(body), headers=headers)
    resp = client.getresponse()
    assert resp.status == 200

    return json.load(resp).get('token')

def update_readme(readme, repo, token):
    """
    Update the full description using contents from the specified readme file.
    """
    with open(readme) as fpin:
        description = fpin.read()

    url = "https://cloud.docker.com/v2/repositories/{:s}/".format(repo)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "JWT {:s}".format(token),
    }
    body = {
        "registry": "registry-1.docker.io",
        "full_description": description,
    }

    client = HTTPSConnection("cloud.docker.com")
    client.request("PATCH", url, body=json.dumps(body), headers=headers)
    resp = client.getresponse()
    assert resp.status == 200

if __name__ == '__main__':
    repo = sys.argv[1]
    readme = sys.argv[2]
    username = os.environ.get('DOCKER_USERNAME')
    password = os.environ.get('DOCKER_PASSWORD')
    token = login(repo, username, password)
    update_readme(readme, repo, token)
