from space_network_lib import (SpaceEntity, Packet, SpaceNetwork, TemporalInterferenceError,
                               DataCorruptedError)
import time
class Satellite(SpaceEntity):

    def receive_signal(self, packet: Packet):
        print(f'{self.name} received signal {packet}')


space = SpaceNetwork(level=2)
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

transmission_attempt(paket)
print(paket)
print(satellite2.receive_signal(paket))
