import sys, os
import request
import traceback

agent = request.default_agent
istart = sys.argv[1]

def getsince(filenum):
    if (filenum==0): return 0 # since is then not important
    try:
        tmpfile = open('./data/page_%d.txt'%(filenum))
        for line in tmpfile.readlines(): pass # to read the last line
        return int(line.split(',')[1])
    except e:
        print("Error starting the page_%d"%(filenum+1))
        raise e

if not os.path.isdir('./data/'):
    os.makedirs('./data/')

i = int(istart)
# here we need to get the since param from the last file if possible
since = getsince(i-1)
while True:
    try:
        agent.status = 'Start parsing file #%d'%(i)
        result = agent.get_all_users(i, since)
        content = "\n".join(['%s:%s,%d'%(u['type'][:4], u['login'], u['id']) for u in result])
        x = open('./data/page_%d.txt'%i, 'w')
        x.write(content)
        x.close()
        since = result[-1]['id']
        i += 1
    except:
        print('exception at page_%d'%i)
        traceback.print_exc(file=sys.stdout)
        break
