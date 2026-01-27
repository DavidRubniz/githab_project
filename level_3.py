from space_network_lib import (SpaceEntity, Packet, SpaceNetwork, TemporalInterferenceError,
                               DataCorruptedError, OutOfRangeError, LinkTerminatedError)
import time


class CommsError(Exception):
    pass


class Satellite(SpaceEntity):

    def receive_signal(self, packet: Packet):
        print(f'{self.name} received signal {packet}')

class BrokenConnectionError(CommsError):
    pass

space = SpaceNetwork(level=3)
satellite1 = Satellite('sat1', 100)
satellite2 = Satellite('sat2', 200)
paket = Packet('dfghjklkjhgfds',satellite1, satellite2)

def transmission_attempt(paket: Packet):
    while True:
        try:
            space.send(paket)
            print("Packet sent successfully!")
            break
        except TemporalInterferenceError:
            print('waiting Interference...')
            time.sleep(2)
        except DataCorruptedError:
            print('data corrupted.')
        except LinkTerminatedError:
            raise BrokenConnectionError('link lost')
        except OutOfRangeError:
            raise CommsError('target out of range')
if __name__ == '__main__':
    try:
        transmission_attempt(paket)
    except:
        print('something went wrong')

print(paket)
print(satellite2.receive_signal(paket))
