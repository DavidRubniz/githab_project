from space_network_lib import SpaceEntity, Packet, SpaceNetwork

class Satellite(SpaceEntity):

    def receive_signal(self, packet: Packet):
        print(f'{self.name} received signal {packet}')


space = SpaceNetwork(level=1)
satellite1 = Satellite('sat1', 100)
satellite2 = Satellite('sat2', 200)
paket = Packet('dfghjklkjhgfds',satellite1, satellite2)
space.send(paket)

