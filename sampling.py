'''
This module contains the sampling util functions
'''

import request
import numpy as np

def get_sample(users, takes=10000):
    '''
    Get samples from random distribution
    '''
    samples = np.random.rand(5)
    size = len(users)
    return [users[int(samples[idx]*size)] for idx in range(1, takes)]


def get_users(users, agent):
    '''
    The agent shall be the request agent
    '''
    return [agent.get_user(user) for user in users]

def get_followers(users, agent):
    '''
    Get followers from the request agent
    '''
    followerlist = [[f['login'] for f in agent.get_followers(user)] for user in users]
    emptystr = ''
    maxlen = max(map(followerlist, len))
    for followers in followerlist:
        followers.extend(['']*(maxlen-len(followers)))
    return np.array([np.array(followers) for followers in followerlist])

 
