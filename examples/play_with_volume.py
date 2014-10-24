# Authors: Romain Trachel <romain.trachel@ens.fr>
#
# License: Artistic License (2.0)

import time
import nmx
from nmx.midi import Midi

port_name = 'my volume port'
midiout = Midi()
print 'opening : ' + port_name
midiout.open(port_name)

# volume channel
ch = 0xB0

# command #1
com1 = 1
# command #2
com2 = 2

print 'sleeping 1 sec'
time.sleep(1)
# for each volume value
for val in range(100):
    # command #1 : increase volume 
    midiout.send_message(ch, com1, val)
    # command #2 : decrease volume
    midiout.send_message(ch, com2, 100-val)
    time.sleep(.1)

print 'closing ' + port_name
midiout.close()