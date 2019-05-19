def calcxor(s):
    sum = 47
    a = min(ord(s[0]),len(s)-2)
    for x in s[2:a+2]:
        sum = sum^ord(x)
    return sum

def check_message(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    x = (calcxor(data))
    if x==ord(data[1]):
        return 1
    return 0

def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <msg-file>'.format(argv[0]))
        return -1
    path = argv[1]
    if check_message(path):
        print('valid message')
        return 0
    else:
        print('invalid message')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
