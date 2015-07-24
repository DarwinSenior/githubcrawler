from __future__ import unicode_literals
import requests
from requests.auth import HTTPBasicAuth
import time
import json
from itertools import chain
from datetime import datetime

user = 'DarwinSenior'
token = '18d17ed0296587032e516b5a588c0335d59a5c2f'
agent = 'DarwinSenior'

class RequestAgent(object):
    def __init__(self, user, token, agent):
        self.session = requests.session()
        self.AUTH = HTTPBasicAuth(user, token)
        self.agent = agent

    def request(self, url, method="GET", limit=100, page=1, since=None):
        """
        domain is 'https://api.github.com/'
        For limit and page https://developer.github.com/v3/#pagination
        For agent https://developer.github.com/v3/#user-agent-required
        """
        req = requests.Request(method, 'https://api.github.com'+url)
        req.auth = self.AUTH
        req.headers['User-Agent'] = self.agent
        req.params['per_page'] = limit
        req.params['page'] = page
        return req

    def request_next(self, url, method="GET"):
        req = requests.Request(method, url)
        req.auth = self.AUTH
        req.headers['User-Agent'] = self.agent
        return req

    def response(self, req):
        """
        Assume req will be json data
        """
        res = self.session.send(req.prepare())
        return res

    def check_ratelimit(self, limit_type='core'):
        """
        https://developer.github.com/v3/rate_limit/
        if exceeds the limit, sleep until the next available session
        Using the UTC
        """
        req = self.request('/rate_limit')
        # data = response(req)['resources']
        data = self.response(req).json()
        if data.get('message') == 'Bad credentials':
            raise ValueError('The credential is invalid')
        data = data['resources'][limit_type]

        if (data['remaining']<1):
            now = datetime.utcnow()
            until = datetime.utcfromtimestamp(data['reset'])
            interval = (until-now).total_seconds()
            print("rate limit(%d) reached, sleep until"%(data['limit'], until.ctime()))
            time.sleep(interval)
            print("resume")

    def get_single(self, url):
        """
        For all the github apis that are not set of data
        """
        self.check_ratelimit()
        req = self.request(url)
        res = self.response(req)
        if (res.ok):
            return res.json()
        else:
            res.raise_for_status()

    def get_collection(self, url, limit=0, start_page=1):
        """
        For all the github apis that returns a collection of data,
        since there is a 100 page limit, we have to ask for multiple request
        """
        self.check_ratelimit()
        data = []
        req = self.request(url, page=start_page)
        res = self.response(req)
        count = 0
        while res.links.get('next') and (limit==0 or count<limit-1):
            if not res.ok: res.raise_for_status()
            data.append(res.json())
            nexturl = res.links['next']['url']
            req = self.request_next(nexturl)
            res = self.response(req)
            count += 1
        data.append(res.json())
        return list(chain.from_iterable(data))

    def get_all_users(self, page, since):
        self.check_ratelimit()
        req = self.request('/users')
        req.params['page'] = page
        req.params['since'] = since
        res = self.response(req)
        data = res.json()
        return list(data)


    def get_user(self, username):
        """
        https://developer.github.com/v3/users/ 
        """
        return self.get_single('/users/%s'%username)

    def get_repo(self, username, repo):
        """
        https://developer.github.com/v3/repos/
        """
        return self.get_single('/repos/%s/%s'%(username, repo))
        
    def get_user_repos(self, username):
        """
        http://developer.github.com/v3/users/
        """
        return self.get_collection('/users/%s/repos'%username)

    def get_user_followers(self, username):
        """
        https://developer.github.com/v3/users/followers/
        """
        return self.get_collection('/users/%s/followers'%username)

    def get_repo_stargazers(username, repo):
        return self.get_collection('/repos/%s/%s/stargazers'%(username, repo))
        
    def get_organization(self, orgnization):
        return self.get_single('/orgs/%s'%orgnization)

    def get_user_organizations(self, username):
        return self.get_single('/users/%s/orgs'%username)

    def get_repo_collaborator(self, username, repo):
        return self.get_collection('/repos/%s/%s/collaborators'%(username, repo))

    def get_repo_forks(self, username, repo):
        return self.get_collection('/repos/%s/%s/forks'%(username, repo))

default_agent = RequestAgent(user, token, agent)


