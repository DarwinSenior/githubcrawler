from __future__ import unicode_literals 
from fire_starter import *

gid_default = 0
N_default = 10

if len(sys.argv) >= 3:
    gid = int(sys.argv[1])
    N = int(sys.argv[2])

if len(sys.argv) == 2:
    gid = int(sys.argv[1])
    N = N_default

if len(sys.argv) == 1:
    gid = gid_default
    N = N_default

fire_starter(gid, N)
