import time
from scapy.all import *
import string


WINDOW       = 60
MAX_ATTEMPTS = 15
EPOCH = 120
SYN = 0x02

# Initialize your data structures here
# TODO: Initialize your data structures

history = {} #Dictionary (implements hash set), were ip addresses are keys and values are a list of times this address tried to syn.
             # list is ordered chronologicaly, and cleaned (time stamps before "window" are deleted) each time this address tries to establish a connection.
last_clean = 0
blocked = set()  # We keep blocked IPs in this set


def on_packet(packet):
    """This function will be called for each packet.
    Use this function to analyze how many packets were sent from the sender
    during the last window, and if needed, call the 'block(ip)' function to
    block the sender."""
    # WARNING: You must call block(ip) to do the blocking.
    if ((IP not in packet) or (packet['IP'].src in blocked) or (TCP not in packet) or (packet['TCP'].flags & SYN == 0)): 
        return #we only filter syn packets from unfiltered ip addresses
    addr = packet['IP'].src
    num = record(addr) #record this ip made an attempt to syn
    if (num>MAX_ATTEMPTS): #if more than 15 attempts in the last minute- block
        block(addr)
        del history[addr] #no nead to keep track of this address connection attempts as its blocked
    if (time.time() - last_clean) > EPOCH: #we want to clean the DB once in a while so it will stay lean (we don't care about old data any way)
        clean()

def record(addr):
    """Updates data structure with another time this ip sent a syn, returns number of syn packets in last minute"""
    now = time.time()
    slot = now - WINDOW #we only care about packets sent after this time stamp
    if (addr not in history): #this is the first time we've seen this ip
        history[addr] = [now,]
        return 1
    lst = history[addr] #this ip was already seen, get the list of times it tried to syn with us
    while lst and lst[0]<slot: #clean the list of any old data
        del lst[0]
    lst += [now,] #record this try
    return len(lst) #this is how many attempts were made in the last minute.

def clean():
    """cleans the data structure every epoch, so at any time our "history" database doesn't hold more than EPOCH seconds worth of data"""
    global last_clean
    last_clean = time.time()
    delete = []
    for ip in history:
        if (history[ip][-1] < (last_clean-EPOCH)): #if the last attempt was more than 2 minutes ago we don't care about the data any way
            delete += [ip,] #make list of values to delete, changing dictionary while iterating is problemtaic so we split it 
    for ip in delete:
        del history[ip]

def generate_block_command(ip):
    """Generate a command that when executed in the shell, blocks this IP.

    The blocking will be based on `iptables` and must drop all incoming traffic
    from the specified IP."""
    return ('sudo iptables -A INPUT -s {0} -j DROP'.format(ip))


def block(ip):
    os.system(generate_block_command(ip))
    blocked.add(ip)


def is_blocked(ip):
    return ip in blocked


def main():
    sniff(prn=on_packet)


if __name__ == '__main__':
    main()
