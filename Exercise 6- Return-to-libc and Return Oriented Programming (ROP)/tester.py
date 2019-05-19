import os, sys
from search import GadgetSearch
import addresses
import assemble


def main(argv):
	g = GadgetSearch('./libc.bin')
	print(g.find('inc edx'))
	#print (g.get_format_count('XOR {0}, {0}; ADD {0}, {0}'))
	#print (g.get_register_combos(2, ('eax', 'ebx', 'ecx')))
	#print ("XOR {0}, {0}; ADD {0}, {1}","('eax', 'ebx')")
	#print (g.format_all_gadgets("XOR {0}, {0}; ADD {0}, {0}",('eax', 'ebx')))
	#print (g.find_all("mov eax, -1"))
	#print g.find_all_formats('mov [{0}] , {1}')
	#print (g.find_all("pop edx"))
	#print (g.find_all("pop edx")[0])
	#print (g.find_all("xor eax, eax")[0])
	#print (g.find_all_formats("mov esp, ebp"))
	#print (g.find_all("mov [edx], eax")[0])
	#print (g.find_all("mov eax, 1")[1])
	#search = GadgetSearch(LIBC_DUMP_PATH)
	


	#print(assemble.assemble_data('mov eax , DWORD PTR [eax+0x58]'))
	#print(assemble.assemble_data('pop eax'))
	#print(hex(3083835809))
	#mov = (assemble.assemble_data('mov edx,ebp'))
	#print ":".join("{:02x}".format(ord(c)) for c in mov)
	#inc = (assemble.assemble_data('inc edx'))
	#print ":".join("{:02x}".format(ord(c)) for c in inc)





if __name__ == '__main__':
    main(sys.argv)
