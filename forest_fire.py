from __future__ import unicode_literals 
import numpy as np
from crawling_functions import *
from db_funcs import *
import os
import random

def isRepo(x):
    return "/" in x

def forest_fire(seed, N, Q, Tu, Td, n, start_time, gid):

    print "Starting fire from SEED "+str(seed)+" ..."
    Q = map(unicode, Q)
    while Q and n<N:
        x = str(Q[0])
        Nsample = np.random.geometric(0.5)
        if isRepo(x):
            print "Crawling deign (%s)"%(str(n))
            new_design = crawl_repo(x, start_time, gid)
            if new_design:
                put_repo(new_design)
                L = new_design['<liked_by>']
                C = new_design['<shot_by>']
            else:
                L = []
                C = []

            L = [l[0] for l in L]
            C = [c[0] for c in C]
            users = [z for z in (L+C) if z in Tu.keys()]
        
            for u in users:
                try:
                    Tu[u].remove(x)
                except:
                    print ' Already removed!'

            if users:
                L = [l for l in L if l not in users]
                C = [l for l in C if l not in users]

            Td[x] = L+C
            # print("L: %s"%(str(L)))
            if Nsample>=len(L):
                Q += L
            else:
                Q += random.sample(L, Nsample)
            Q = Q+C
        elif x:
            print "Crawling User (%s) "%(str(n))

            new_user = crawl_user(x, start_time, gid)
            if new_user:
                put_user(new_user)
                L = new_user['<likes>']
                C = new_user['<shots>']
            else:
                L = []
                C = []

            L = [z[0] for z in L]
            C = [c[0] for c in C]
            designs = [z for z in (L+C) if z in Td.keys()]
            for d in designs:
                try:
                    Td[d].remove(x)
                except:
                    print 'Already removed!'
            if designs:
                L = [z for z in L if z not in designs]
                C = [z for z in C if z not in designs]
            LC = L+C
            Tu[x] = LC

            if Nsample>=len(LC):
                Q += LC
            else:
                Q += random.sample(LC, Nsample)
        Q.pop(0)
        n += 1
        update_status(seed, Q, Tu, Td, n)
    print "Done with SEED %s !"%str(seed)
    return 0




