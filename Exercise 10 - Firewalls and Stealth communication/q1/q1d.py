from scapy.all import *

SYN = 0x02
def on_packet(packet):
    """Implement this to send a SYN ACK packet for every SYN."""
    # TODO: Implement me
    # WARNING: Use only the `send` function from scapy to send the packet. Do
    #          not use any other function to send/receive packets.
    if ((IP not in packet) or (packet['IP'].dst == '127.0.0.1') or (TCP not in packet) or (packet['TCP'].flags ^ SYN != 0)): #local host packets made a lot of noise
        return #we don't care about packets other than syn
    ansr = IP(dst = packet['IP'].src) / TCP(sport = packet['TCP'].dport, dport = packet['TCP'].sport, flags = 'SA', ack = 1 + packet['TCP'].seq + len(packet['TCP'].payload ))
    send(ansr)


def main(argv):
    sniff(prn=on_packet)


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

