import os, sys
from assemble import assemble_file

PATH_TO_SUDO = './sudo'
PATH_TO_ASM = 'shellcode.asm'


def run_shell():
    # Your code here
    pw = assemble_file(PATH_TO_ASM)
    os.execl(PATH_TO_SUDO, "" ,pw ,"") 
    raise NotImplementedError()


def main(argv):
    if not len(argv) == 1:
        print 'Usage: %s' % argv[0]
        sys.exit(1)

    run_shell()


if __name__ == '__main__':
    main(sys.argv)
