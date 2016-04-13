from __future__ import unicode_literals
import request
import traceback
from datetime import datetime
from requests import HTTPError
from fire_tracker import *
import time

agent = request.RequestAgent('', '', '')

def tryGet(func, default):
    for i in range(10):
        try:
            x = func()
            return x
        except HTTPError,err:
            print(err)
            print('===========')
            time.sleep(1)
            continue
    return default
def is_before_start_time(dribbble_time, start_time, tform = '%Y-%m-%dT%H:%M:%SZ'):                             
    return datetime.strptime(dribbble_time,tform) < datetime.strptime(start_time,tform)

def filter_like(like, shot):
    likesset = set(x[0] for x in shot)
    return [x for x in like if x[0] not in likesset]

def repoClean(repodata):
    newdata = {}
    for key, value in repodata.iteritems():
        if (key not in ['id', 'name', 'owner', 'private', 'organization',]) and ('url' not in key):
            newdata[key] = value

    return newdata

def userClean(userdata):
    newdata = {}
    for key,value in userdata.iteritems():
        if (key not in ['id', 'gravatar_id',]) and ('url' not in key):
            newdata[key] = value
    return newdata

def userAddLink(userdata, start_time):
    username = userdata['login']
    repos = tryGet(lambda: agent.get_user_repos(username), [])
    try:
        creates = [(repo['full_name'], repo['created_at']) for repo in repos if is_before_start_time(repo['created_at'], start_time)]
    except:
        print repo
        print('creates exception')
        creates = []
    repos = tryGet(lambda: agent.get_user_starred(username), [])

    try:
        stars = [(repo['repo']['full_name'], repo['starred_at']) for repo in repos if is_before_start_time(repo['starred_at'], start_time)]
    except:
        print repo
        print('stars exception')
        stars = []

    stars = filter_like(stars, creates)
    userdata['<shots>'] = creates
    userdata['<likes>'] = stars
    return userdata

def repoAddLink(repodata, start_time):
    username,repo = repodata['full_name'].split('/')
    users = tryGet(lambda:agent.get_repo_stargazers(username, repo), [])
    try:
        stargazers = [(user['user']['login'], user['starred_at']) for user in users if is_before_start_time(user['starred_at'], start_time)]
    except:
        print('startgazer wrong: user')
        print user
        stargazers = []
    user = tryGet(lambda:agent.get_user(username), None)
    creators = [(user['login'], user['created_at'])] if user else []

    stargazers = filter_like(stargazers, creators)
    repodata['<shot_by>'] = creators
    repodata['<liked_by>'] = stargazers
    return repodata

def crawl_repo(x, start_time, gid):
    print "crawling repo %s"%x
    username, repo = x.split('/')
    try:
        repodata = tryGet(lambda: agent.get_repo(username, repo), None)
        repodata = repoAddLink(repodata, start_time)
        repodata = repoClean(repodata)
    except HTTPError, err:
        repodata = None
        print('repo %s does not exists'%x)
        print(err)
        traceback.print_exc()
        raw_input('')
    return repodata

def crawl_user(x, start_time, gid):
    print "crawling user %s"%x
    username = x
    try:
        userdata = tryGet(lambda: agent.get_user(username), None)
        userdata = userAddLink(userdata, start_time)
        userdata = userClean(userdata)
    except HTTPError, err:
        userdata = None
        print('user %s does not exist'%x)
        print(err)
        traceback.print_exc()
        raw_input("")
    return userdata
