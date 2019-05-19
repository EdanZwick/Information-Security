from scapy.all import *


OPEN = 'open'
CLOSED = 'closed'
FILTERED = 'filtered'


def generate_syn_packets(ip, ports):
    """Returns a list of TCP SYN packets, to perform a SYN scan on the given
       TCP ports."""
    lst = []
    for p in ports:
    	lst += IP(dst = ip) / TCP(dport = p , flags = 'S') #append a packet with requested dport
    return lst


def analyze_scan(ip, ports, answered, unanswered):
    """Analyze the results from `sr` of SYN packets.
    
    This function returns a dictionary from port number, to
    'open' / 'closed' / 'filtered', based on the answered and unanswered packets
    return from `sr`.
    """
    results = dict()
    SA = 0x02 | 0x10 #syn and ack flags bit value
    for ans in answered:
    	p = ans[1]
    	if not TCP in p:
    		continue
    	if (p['TCP'].flags ^ SA) == 0: #what we expect to recieve from an open port
    		results[p['TCP'].sport]=OPEN
    	else: #if we got anything else, tipicaly a RA
    		results[p['TCP'].sport]=CLOSED
    for p in unanswered:
    	if not TCP in p:
    		continue
    	results[p['TCP'].dport]= FILTERED
    return results
    

def stealth_syn_scan(ip, ports, timeout):
    # WARNING: DO NOT MODIFY THIS FUNCTION
    packets = generate_syn_packets(ip, ports)
    answered, unanswered = sr(packets, timeout=timeout)
    return analyze_scan(ip, ports, answered, unanswered)


def main(argv):
    # WARNING: DO NOT MODIFY THIS FUNCTION
    if not 3 <= len(argv) <= 4:
        print('USAGE: %s <ip> <ports> [timeout]' % argv[0])
        return 1
    ip    = argv[1]
    ports = [int(port) for port in argv[2].split(',')]
    if len(argv) == 4:
        timeout = int(argv[3])
    else:
        timeout = 5
    results = stealth_syn_scan(ip, ports, timeout)
    for port, result in results.items():
        print('port %d is %s' % (port, result))


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
