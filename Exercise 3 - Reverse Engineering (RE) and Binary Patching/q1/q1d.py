def patch_program(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    l = list(data)
    l[1739] = chr(235)
    data = ''.join(l)
    with open(path + '.patched', 'wb') as writer:
        writer.write(data)


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <msgcheck-program>'.format(argv[0]))
        return -1
    path = argv[1]
    patch_program(path)
    print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
