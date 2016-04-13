import request
import sampling as sp
import numpy as np

agent = request.default_agent

np.save('follwer_bin.npy', sp.getuserseeds(agent))
