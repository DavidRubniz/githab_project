from space_network_lib import (SpaceEntity, Packet, SpaceNetwork, TemporalInterferenceError,
                               DataCorruptedError, OutOfRangeError, LinkTerminatedError)
import time


class CommsError(Exception):
    pass

class RelayPacket(Packet):
    def __init__(self, packet_to_relay, sender, proxy):
        super().__init__(packet_to_relay, sender, proxy)
    def __repr__(self):
        return f'Relaying[{self.data}] to {self.receiver} from {self.sender}'


class Satellite(SpaceEntity):

    def receive_signal(self, packet: Packet):
        if isinstance(packet, RelayPacket):
            inner_paket = packet.data
            print(f"Unwrapping and forwarding to {inner_paket.receiver}")
            if isinstance(inner_paket, Packet):
                transmission_attempt(inner_paket)
                return
            self.receive_signal(inner_paket)
        else:
                print(f'{self.name} received signal {packet}')

class BrokenConnectionError(CommsError):
    pass

space = SpaceNetwork(level=4)
satellite1 = Satellite('sat1', 100)
satellite2 = Satellite('sat2', 200)
satellite3 = Satellite('sat3', 300)
satellite4 = Satellite('sat4', 400)
earth  = Satellite('earth', 0)
paket = Packet('dfghjklkjhgfds',satellite3, satellite4)
paket_to_relay_to_1 = RelayPacket(paket, satellite1, satellite2)
paket_to_relay_to_2 = RelayPacket(paket, satellite2, satellite3)



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
        transmission_attempt(paket_to_relay_to_1)
    except Exception as e:
        print(f'Critical Error: {e}')

