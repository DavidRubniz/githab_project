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

def smart_send_packet(packet: Packet, spaces: list[SpaceEntity]):
    source = packet.sender.distance_from_earth
    destination = packet.receiver.distance_from_earth
    if destination - source < 150:
        return packet
    next_source = next(
        sat for sat in spaces if sat.distance_from_earth > source and sat.distance_from_earth < source + 150)
    new_packet = Packet(data=packet.data, sender=next_source, receiver=packet.receiver)
    f = smart_send_packet(new_packet, spaces)
    return RelayPacket(f, packet.sender, next_source)

def sender_(packet: Packet, spaces: list[SpaceEntity]):
    p = smart_send_packet(packet, spaces)
    transmission_attempt(p)

class BrokenConnectionError(CommsError):
    pass

space = SpaceNetwork(level=4)
satellite1 = Satellite('sat1', 100)
satellite2 = Satellite('sat2', 200)
satellite3 = Satellite('sat3', 300)
satellite4 = Satellite('sat4', 400)
earth  = Satellite('earth', 0)
paket = Packet('dfghjklkjhgfds', earth, satellite4)
paket_to_relay_to_1 = RelayPacket(paket, satellite1, satellite2)
paket_to_relay_to_2 = RelayPacket(paket, satellite2, satellite3)

spaces = [satellite1, satellite2, satellite3, satellite4]

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
        sender_(paket, spaces)
    except Exception as e:
        print(f'Critical Error: {e}')

