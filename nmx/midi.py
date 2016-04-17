# Authors: Romain Trachel <romain.trachel@ens.fr>
#
# License: Artistic License (2.0)

import time
import rtmidi

class Midi():
    """Midi interface

    Attributes
    ----------
    midiout : rtmidi.MidiOut Object
    
    """
    def __init__(self):
        self.midiout = rtmidi.MidiOut()
    
    """Open a midi port

    Parameters
    ----------
    pname : Port name 
        "virtual output" (default)
    
    """
    def open(self, pname='virtual output'):
        available_ports = self.midiout.get_ports()
        
        if False:#available_ports:
            self.midiout.open_port(0)
        else:
            self.midiout.open_virtual_port(pname)
        
    
    def send_message(self, chan, com, val):
        """Send a midi message

        Parameters
        ----------
        chan : channel (int)
        com  : command (int)
        val  : value (int)
        
        """
        self.midiout.send_message([chan, com, val])
    
    def close(self):
        self.midiout.close_port()
    