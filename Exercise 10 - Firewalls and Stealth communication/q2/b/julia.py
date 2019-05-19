import socket
from Crypto.Cipher import AES

KEY = 'FreedomIsSlavery' #pre-shared key, if they weren't so indoctrinated they probably should have choosen a random sequnce...
BLOCK_BYTES = 16 #pre-defined

def receive_message(port):
    # TODO: Reimplement me! (question 2b)
    listener = socket.socket()
    try:
        listener.bind(('', port))
        listener.listen(1)
        connection, address = listener.accept()
        try:
            msg = connection.recv(1024)
            ciphertext , iv = parse(msg) #the transmition includes the iv and the cyphertext- split them
            plaintext = AES.new(KEY, AES.MODE_CBC, iv).decrypt(ciphertext)
            return unpad(plaintext) #remove the padding, custom function
        finally:
            connection.close()
    finally:
        listener.close()

def parse(msg):
    # Recieves a payload and splits it into cypher text and iv
    # In 1984 protocol, the transmition ends with iv (which is always the size of the key) and then the cyphertext itself
    iv = msg[len(msg)-BLOCK_BYTES:]
    ciphertext = msg[:len(msg)-BLOCK_BYTES]
    return ciphertext , iv

def unpad(msg):
    #Remove the PKCS7 padding from message.
    #****Assumes there is at least 1 byte of padding, ie each message is 15 bytes or less***** 
    pad_len = ord(msg[-1])
    return msg[:len(msg)-pad_len]

def main():
    message = receive_message(1984)
    print('received: %s' % message)


if __name__ == '__main__':
    main()
