from __future__ import unicode_literals 
import sys, traceback
from forest_fire import *

def disp_runtime():
    print ""
    print "======================="
    print datetime.utcnow()-datetime.strptime(get_start_time(), '%Y-%m-%dT%H:%M:%SZ')
    print "======================="

def fire_starter(gid, N):
    seedQ = get_seedQ(gid)
   
  
    try:
        while seedQ:
            seed = seedQ[0]
            Q, Tu, Td, n = get_status(seed)
            if len(Q) == 0:
                # raw_input('')
                seedQ.remove(seed)
            elif n>=N:
                record_n(seed,n=0)
                seedQ = seedQ[1:]+seedQ[:1]
            else:
                status_flag = forest_fire(seed, N, Q, Tu, Td, n, get_start_time(), gid)
                if status_flag == -911:
                    break
                seedQ = seedQ[1:]+seedQ[:1]
            record_seedQ(seedQ, gid)
    except:
        traceback.print_exc(file=sys.stdout)
    disp_runtime()
