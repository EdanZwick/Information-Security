from scapy.all import *


LOVE = 'love'
unpersons = set()


def spy(packet):
    """Check for love packets.

    For each packet containing the word 'love', add the sender's IP to the
    `unpersons` set.
    """
    # TODO: Implement me (question 2a)
    try:
	    if ((IP not in packet) or (TCP not in packet) or (Raw not in packet)): #not ip or doesn't have a payload
	    	return
	    if (packet['Raw'].load.find(LOVE)>0): #does the payload contain love
	    	unpersons.add(packet['IP'].src)
    except:
    	return

def main():
    sniff(prn=spy)


if __name__ == '__main__':
    main()
