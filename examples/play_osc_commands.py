# Authors: Romain Trachel <romain.trachel@ens.fr>
#
# License: Artistic License (2.0)

import time
import nmx
from random import random
from simpleOSC import initOSCClient, initOSCServer, setOSCHandler, sendOSCMsg, closeOSC, \
        createOSCBundle, sendOSCBundle, startOSCServer


ip = "127.0.0.1"
client_port = 8001

# takes args : ip, port
initOSCClient(ip=ip, port=client_port)

# takes args : ip, port, mode --> 0 for basic server, 1 for threading server, 2 for forking server
initOSCServer(ip=ip, port=6400)

# and now set it into action
startOSCServer()

for x in range(100):
    try:
        # !! it sends by default to localhost ip "127.0.0.1" and port 9000 
        sendOSCMsg("/nmx/test/", [random.random()])
        # create and send a bundle
        bundle = createOSCBundle("/nmx/test/x")
        # 1st message appent to bundle
        bundle.append(666)
        # 2nd message appent to bundle
        bundle.append("the number of the beast")
        # !! it sends by default to localhost ip "127.0.0.1" and port 9000 
        sendOSCBundle(bundle)
        # you don't need this, but otherwise we're sending as fast as possible.
        time.sleep(0.5)
    except KeyboardInterrupt:
        print "closing all OSC connections... and exit"
        # finally close the connection before exiting or program.
        closeOSC()
