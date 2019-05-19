import math
from scapy.all import *


LOVE = 'love'
unpersons = set()


def spy(packet):
    """Check for love packets and encrypted packets.

    For each packet containing the word 'love' (or a packet which is encrypted),
    add the sender's IP to the `unpersons` set.
    """
    # TODO: Implement me (question 2c)
    try:
        if ((IP not in packet) or (TCP not in packet) or (Raw not in packet)): #not ip\TCP or doesn't have a payload
            return
        if (packet['Raw'].load.find(LOVE)>0 or entropy(packet['Raw'].load)>3.0): #does the payload contain love or is suspected to be encrypted
            unpersons.add(packet['IP'].src)
    except:
        return


def entropy(string):
    distribution = [float(string.count(c)) / len(string)
                    for c in set(string)]
    return -sum(p * math.log(p) / math.log(2.0) for p in distribution)


def main():
    sniff(prn=spy)


if __name__ == '__main__':
    main()
