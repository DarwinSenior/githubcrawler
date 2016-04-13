'''
This module contains the sampling util functions
'''

from __future__ import unicode_literals
import request
import numpy as np
import json
import os
from itertools import chain

def get_sample(users, takes=10000):
    '''
    Get samples from random distribution
    '''
    samples = np.random.rand(5)
    size = len(users)
    return [users[int(samples[idx]*size)] for idx in range(1, takes)]

def getuser(idx):
    pageidx = int(idx/100)
    lineidx = int(idx%100)
    page = open('data/page_%i.txt'%(pageidx+1), 'r')
    line = page.readlines()[lineidx]
    user = line[5:].split(',')[0]
    page.close()
    return user

total_users = (13011701)
sample_size = 10000


def combineuserdata():
    i = 0 
    data = []
    while True:
        if os.path.isfile('userdata/users%i.json'%i):
            with open('userdata/users%i.json'%i, 'r') as userfile:
                datum = json.load(userfile)
                data.append(datum)
                print('combining file #%i'%i)
                i += 1
        else:
            break
    with open('userdata/users_til_%i.json'%(i-1), 'w') as userfile:
        json.dump(list(chain.from_iterable(data)), userfile)
    return

def getuserseeds(agent, sample_size=sample_size, random_user=None):
    i = 0
    random_users = random_user or set()
    user_data = []
    while i<sample_size:
        idx = np.random.randint(0, total_users)
        username = getuser(idx)
        level = int(i/1000)
        if (username in random_users): continue
        try:
            data = agent.get_user(username)
            data = cleanuser(data)
            user_data.append(data)
            print('get user #%i name: %s'%(i, username))
            random_users.add(username)
            with open('userdata/usedname.json', 'w') as usersfile:
                json.dump(list(random_users), usersfile)
            with open('userdata/users%i.json'%(level), 'w') as usersfile:
                json.dump(user_data[level*1000:], usersfile)
            i += 1
        except:
            print('user %s is 404'%username)
            continue


# def getuserseeds(agent):
#     random_idxs = np.random.choice(
#             range(total_users),
#             sample_size,
#             False)
#     random_users = map(getuser, random_idxs)
#     with open('random_users.json', 'w') as tmpfile:
#         json.dump(random_users, tmpfile)
    
    # users_data = []
    # print('start to get users')
    # for i,user in enumerate(random_users):
    #     agent.status = 'get user %d'%i
    #     print('get user #%d name#%s'%(i, user))
    #     user_data = agent.get_user(user)
    #     user_data = cleanuser(user_data)
    #     users_data.append(user_data)
    #     with open('progress.json', 'w') as progressfile:
    #         json.dump(users_data, progressfile)
        
    # follower_bins = followers_bin(users_data)
    # return follower_bins

def cleanuser(userdata):
    cleaneddata = {}
    for key,val in userdata.iteritems():
        if (not 'url' in key) and (key != 'gravatar_id'):
            cleaneddata[key] = val
    return cleaneddata
def get_users(users, agent):
    '''
    The agent shall be the request agent
    '''
    return [agent.get_user(user) for user in users]

def followers_bin(users):
    maxfollowers = max([user['following'] for user in users])
    x = [[] for i in range(0, maxfollowers+1)]
    for user in users:
        x[user['following']].append(user['login'])
    return x

def get_followers(users, agent):
    '''
    Get followers from the request agent
    '''
    followerlist = [[f['login'] for f in agent.get_user_followers(user)] for user in users]
    emptystr = ''
    maxlen = max(map(followerlist, len))
    for followers in followerlist:
        followers.extend(['']*(maxlen-len(followers)))
    return followers

 
