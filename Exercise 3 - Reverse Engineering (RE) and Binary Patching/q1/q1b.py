from q1a import calcxor

def fix_message(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    x = calcxor(data)
    s = list(data)    
    s[1] = chr(x)
    data = ''.join(s)
    with open(path + '.fixed', 'wb') as writer:
        writer.write(data)


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <msg-file>'.format(argv[0]))
        return -1
    path = argv[1]
    fix_message(path)
    print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
