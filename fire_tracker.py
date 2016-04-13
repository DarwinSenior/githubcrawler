from __future__ import unicode_literals 
import json, os, time
from random import randint

def record_msg(msg, gid, datapath='./fire_tracker/'):
    if not os.path.isdir(datapath):
        os.makedirs(datapath)
    with open(datapath+'msg'+str(gid)+'.txt', 'wb') as f:
        f.write(str(msg))

def get_start_time(datapath='./fire_tracker/'):
    with open(datapath+'start_time.txt', 'rb') as f:
        start_time = f.read()
    return start_time

def record_start_time(start_time, datapath='./fire_tracker/'):
    if not os.path.isdir(datapath):
        os.makedirs(datapath)
    with open(datapath+'start_time.txt', 'wb') as f:
        f.write(start_time)

def read_auths(datapath='./inputs/'):
    with open(datapath+'auths.txt', 'rb') as f:
        auths = f.read().splitlines()
    return auths

def get_authQ(gid, datapath='./fire_tracker/'):
    with open(datapath+'authQ'+str(gid)+'.txt', 'rb') as f:
        authQ = f.read().splitlines()
    return authQ

def record_authQ(authQ, gid, datapath='./fire_tracker/'):
    if not os.path.isdir(datapath):
        os.makedirs(datapath)
    with open(datapath+'authQ'+str(gid)+'.txt', 'wb') as f:
        f.write('\n'.join(authQ))

def read_seeds(datapath='./inputs/'):
    with open(datapath+'seeds.txt', 'rb') as f:
        seeds = f.read().splitlines()
    return seeds

def get_seedQ(gid, datapath='./fire_tracker/'):
    with open(datapath+'seedQ'+str(gid)+'.txt', 'rb') as f:
        seedQ = f.read().splitlines()
    return seedQ

def record_seedQ(seedQ, gid, datapath='./fire_tracker/'):
    if not os.path.isdir(datapath):
        os.makedirs(datapath)
    with open(datapath+'seedQ'+str(gid)+'.txt', 'wb') as f:
        f.write('\n'.join(seedQ))

def get_api_counter(datapath='./fire_tracker/'):
    with open(datapath+'api_counter.txt', 'rb') as f:
        n = int(f.read())
    return n

def get_Q(seed, datapath='./fire_tracker/'):
    with open(datapath+seed+'/Q.txt', 'rb') as f:
        Q = f.read().splitlines()
    return Q

def get_Tu(seed, datapath='./fire_tracker/'):
    with open(datapath+seed+'/Tu.txt', 'rb') as f:
        Tu = json.loads(f.read())
    return Tu

def get_Td(seed, datapath='./fire_tracker/'):
    with open(datapath+seed+'/Td.txt', 'rb') as f:
        Td = json.loads(f.read())
    return Td

def get_n(seed, datapath='./fire_tracker/'):
    with open(datapath+seed+'/n.txt', 'rb') as f:
        n = int(f.read())
    return n


def record_api_counter(n=0, datapath='./fire_tracker/'):
    if not os.path.isdir(datapath):
        os.makedirs(datapath)
    with open(datapath+'api_counter.txt', 'wb') as f:
        f.write(str(n))

def record_Q(seed, Q=[], datapath='./fire_tracker/'):
    path = datapath+seed
    if not os.path.isdir(path):
        os.makedirs(path)
    with open(path+'/Q.txt', 'wb') as f:
        f.write('\n'.join(Q))

def record_Tu(seed, Tu={}, datapath='./fire_tracker/'):
    path = datapath+seed
    if not os.path.isdir(path):
        os.makedirs(path)
    with open(path+'/Tu.txt', 'wb') as f:
        f.write(json.dumps(Tu))

def record_Td(seed, Td={}, datapath='./fire_tracker/'):
    path = datapath+seed
    if not os.path.isdir(path):
        os.makedirs(path)
    with open(path+'/Td.txt', 'wb') as f:
        f.write(json.dumps(Td))

def record_n(seed, n=0, datapath='./fire_tracker/'):
    path = datapath+seed
    if not os.path.isdir(path):
        os.makedirs(path)
    with open(path+'/n.txt', 'wb') as f:
        f.write(str(n))


def init_status(seed):
    record_Q(seed,Q=[seed])
    record_Tu(seed)
    record_Td(seed)
    record_n(seed)

def update_status(seed, Q, Tu, Td, n):
    record_Q(seed, Q)
    record_Tu(seed, Tu)
    record_Td(seed, Td)
    record_n(seed, n)

def get_status(seed):
    Q = get_Q(seed)
    Tu = get_Tu(seed)
    Td = get_Td(seed)
    n = get_n(seed)
    return Q, Tu, Td, n

def api_add1():
    #record_api_counter(get_api_counter()+1)
    time.sleep(randint(5,10))


# database
def design_deposit(design, gid, datapath='./database/'):
    filename = datapath+'designs'+str(gid)+'.json';
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            data = json.load(f)
    else:
        if not os.path.isdir(datapath):
            os.makedirs(datapath)
        data = {}
    data[str(design['id'])] = design
    with open(filename, 'wb') as f:
        json.dump(data,f)

def user_deposit(user, gid, datapath='./database/'):
    filename = datapath+'users'+str(gid)+'.json';
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            data = json.load(f)
    else:
        if not os.path.isdir(datapath):
            os.makedirs(datapath)
        data = {}
    data[str(user['username'])] = user
    with open(filename, 'wb') as f:
        json.dump(data,f)
