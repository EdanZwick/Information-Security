import assemble

def tester():
	print ":".join("{:02x}".format(ord(c)) for c in (assemble.assemble_data("xor eax,eax ; ret \n")))

if __name__ == '__main__':
	tester()