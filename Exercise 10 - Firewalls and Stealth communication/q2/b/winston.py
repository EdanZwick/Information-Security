import socket
from Crypto.Cipher import AES
import os

KEY = 'FreedomIsSlavery' #pre-shared key, if they weren't so indoctrinated they probably should have choosen a random sequnce...
MESSAGE = 'I love you'
BLOCK_BYTES = 16

def send_message(ip, port):
    # TODO: Reimplement me! (question 2b)
    padded_data = pad(MESSAGE) #get padded message
    iv = os.urandom(BLOCK_BYTES) #generate random iv
    ciphertext = AES.new(KEY, AES.MODE_CBC, iv).encrypt(padded_data) #encrypt
    msg = ciphertext + iv #add iv as per protocol
    connection = socket.socket()
    try:
        connection.connect((ip, port))
        connection.send(msg)
    finally:
        connection.close()

def pad(msg):
	#Adds the PKCS7 padding from message.
    #****Assumes message is 15 bytes or less***** 
	pad_len = BLOCK_BYTES - len(msg)
	return msg + (chr(pad_len) * pad_len) 

def main():
    send_message('127.0.0.1', 1984)


if __name__ == '__main__':
    main()
