import assemble

def patch_program(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    p1 = assemble.assemble_file("patch1.asm")
    patch1 = list(p1)
    p2 = assemble.assemble_file("patch2.asm")
    patch2 = list(p2)
    l = list(data)
    l = l[0:1485] + patch2 +l[1485+len(patch2):1587] + patch1 + l[1587+len(patch1):]
    data = ''.join(l)
    with open(path + '.patched', 'wb') as writer:
        writer.write(data)


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <readfile-program>'.format(argv[0]))
        return -1
    path = argv[1]
    patch_program(path)
    print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
