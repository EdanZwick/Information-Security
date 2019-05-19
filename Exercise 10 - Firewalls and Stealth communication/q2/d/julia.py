from scapy.all import *
import socket
import binascii

SPORT = 65000 #predefined between winston and julia
SYN = 0x02

def receive_message(port):
    i = 0
    msg = ''
    left = True
    while left: #ugly but no do-while loop in python (saves duplicate code to recieve first packet)
        p = sniff(count = 1, lfilter= (lambda packet : filter(packet,i)))[0] #wait for next packet in sequence
        msg += "{:0>3b}".format(p['TCP'].reserved) #add payload to binary string (formatting used to make sure exactly 3 bits are added and 0's are not omitted)
        i+=1 #update the counter for recieved
        if i == p['TCP'].ack:
            left = False #this was the last packet
        ack(p,port) #ack so Winston will send next packet
    return decoder(msg)
    
def filter(packet,i):
    #Static filter to get only packets from winston. we combine this with a check for the wanted seq number as filter in sniff function
    if (IP not in packet) or (TCP not in packet) or (packet['TCP'].sport != SPORT) or (packet['TCP'].flags ^ SYN !=0) or (packet['TCP'].seq != i):
        return False
    return True

def decoder(msg):
    #Translate the recieved bit string back to text
    l = len(msg)
    msg = msg[:l-(l%8)] #get rid of padding
    n = int(msg, 2)
    return binascii.unhexlify('%x' % n) #from stack overflow, translates this int back to a string

def ack(p,port):
    #acks winston we recieved this packet and he can send the next one
    send(IP(dst = p['IP'].src) / TCP(sport = port, dport = SPORT, flags = 'SA', ack = p['TCP'].seq), verbose=0)

def main():
    message = receive_message(1984)
    print('received: %s' % message)

if __name__ == '__main__':
    main()

