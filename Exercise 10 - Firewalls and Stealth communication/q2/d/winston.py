from scapy.all import *
import socket
import binascii

MESSAGE = 'I love you'

def send_message(ip, port):
    msg = encode(MESSAGE)
    num_mes = len(msg) / 3 #encode function makes sure this is devisable by 3
    template = IP(dst=ip) / TCP(sport = 65000, dport = port , ack = num_mes) #we'll send this packet just editing the seq and reserved bits each time
    i = 0
    while i < num_mes:
 		sr1(payload(msg,i,template), verbose=0) #send message untill ack from julia
 		i += 1

def payload(msg,i,template):
	#creates the next message to send (after an ack was recieved for the previous one)
	index = i*3 #the starting bit of this message
	template['TCP'].seq = i #number of bit in this message
	template['TCP'].reserved = int(msg[index:index+3],2) #convert bits string to int in range (0-7)
	return template

def encode(msg):
	#translates a string to it's binary representation (still in string form)
	tmp = ''.join("{:0>8b}".format(ord(x), 'b') for x in msg) #from stack overflow
	tmp += '0' * (3 - (len(tmp)%3)) #pads to a multiple of 3
	return tmp

def main():
    send_message('127.0.0.1', 1984)


if __name__ == '__main__':
    main()
