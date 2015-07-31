# from __future__ import unicode_literals 
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('localhost', 27017)
db = client['github-db']

def repos():
    return db['repos-%s'%(str(datetime.today()))]

def users():
    return db['users-%s'%(str(datetime.today()))]

def delete_repo(repo_name):
    repos().find_one_and_delete({
            'name': repo_name,
        })

def delete_user(user_name):
    users().find_one_and_delete({
            'name': user_name,
        })

def get_repo(repo_name):
    return repos().find_one({'full_name': repo_name})

def get_user(user_name):
    return users().find_one({'login': user_name})

def get_all_user():
    return list(users().find())

def get_all_repo():
    return list(repos().find())

def put_repo(repo):
    repo_name = repo['full_name']
    previous = repos().find_one({'full_name': repo_name})
    if previous:
        print('Update repo "%s"'%repo_name)
        repos().update(
                {'full_name': repo_name},
                {'$set': repo},
                upsert=False)
    else:
        print('Insert repo "%s"'%repo_name)
        repos().insert(repo)

def put_user(user):
    user_name = user['login']
    previous = users().find_one({'login': user_name})
    if previous:
        print('Update user %s'%user_name)
        users().update(
                {'login': user_name},
                {'$set': user},
                upsert=False)
    else:
        print('Insert user %s'%user_name)
        users().insert(user)

def put_repos(repos):
    for repo in repos:
        put_repo(repo)

def put_users(users):
    for user in users:
        put_user(user)
