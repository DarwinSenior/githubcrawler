from __future__ import unicode_literals 
import os
from datetime import *
from fire_tracker import *

if not os.path.isdir('./fire_tracker/'):
    #record_api_counter(n=0)
    record_start_time(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))
    seeds = read_seeds()
    auths = read_auths()
    Ns = len(seeds)
    Na = len(auths)
    Ng = 5
    for seed in seeds:
        init_status(seed)
    for i in range(Ng):
        record_seedQ([seeds[k] for k in range(i,Ns,Ng)],i)
        record_authQ([auths[k+3*i] for k in range(Na/Ng)],i)
    print "Initialized with "+str(Ns)+" seeds and "+str(Ng)+" seed groups!"
else:
    print "Already initialized!"
