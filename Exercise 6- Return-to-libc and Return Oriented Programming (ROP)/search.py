import addresses
import assemble
import string, itertools


GENERAL_REGISTERS = [
    'eax', 'ebx', 'ecx', 'edx', 'esi', 'edi'
]


ALL_REGISTERS = GENERAL_REGISTERS + [
    'esp', 'eip', 'ebp'
]


class GadgetSearch(object):
    def __init__(self, dump_path, start_addr=None):
        """
        Construct the GadgetSearch object.

        Input:
            dump_path: The path to the memory dump file created with GDB.
            start_addr: The starting memory address of this dump. Use
                        `addresses.LIBC_TEXT_START` by default.
        """
        self.start_addr = (start_addr if start_addr is not None
                           else addresses.LIBC_TEXT_START)
        with open(dump_path, 'rb') as f:
            self.dump = f.read()

    def get_format_count(self, gadget_format):
        """
        Get how many different register placeholders are in the pattern.
        
        Examples:
            self.get_format_count('POP ebx')
            => 0
            self.get_format_count('POP {0}')
            => 1
            self.get_format_count('XOR {0}, {0}; ADD {0}, {1}')
            => 2
        """
        # Hint: Use the string.Formatter().parse method:
        #
        #   import string
        #   print string.Formatter().parse(gadget_format)
        
        tmp = string.Formatter().parse(gadget_format) #iterator on tokens from original string, each token is a tupple with 3 elements. [1] is the format value
        s = set([x[1] for x in tmp]) #goes over the format values in each tupple and gets rid of duplicities
        if None in s: #string ending with text will produce one extra tuple
        	return len(s)-1 
        return len(s)
        #raise NotImplementedError()

    def get_register_combos(self, nregs, registers):
        """
        Return all the combinations of `registers` with `nregs` registers in
        each combination. Duplicates ARE allowed!

        Example:
            self.get_register_combos(2, ('eax', 'ebx'))
            => [['eax', 'eax'],
                ['eax', 'ebx'],
                ['ebx', 'eax'],
                ['ebx', 'ebx']]
        """
        s = set(registers)
        tmp = list(itertools.product(s,repeat = nregs)) #produces a crteasian product of elements, as a tuple
        return [list(elem) for elem in tmp] #convert the values to lists (instead of tuples)
        #raise NotImplementedError()

    def format_all_gadgets(self, gadget_format, registers):
        """
        Format all the possible gadgets for this format with the given
        registers.

        Example:
            self.format_all_gadgets("POP {0}; ADD {0}, {1}", ('eax', 'ecx'))
            => ['POP eax; ADD eax, eax',
                'POP eax; ADD eax, ecx',
                'POP ecx; ADD ecx, eax',
                'POP ecx; ADD ecx, ecx']
        """
        # Hints:
        #
        # 0. Use the previous functions to count the number of placeholders,
        #    and get all combinations of registers.
        #
        # 1. Use the `format` function to build the string:
        #
        #    'Hi {0}! I am {1}, you are {0}'.format('Luke', 'Vader')
        #    => 'Hi Luke! I am Vader, you are Luke'
        #
        # 2. You can use pass a list of arguments instead of specifying each
        #    argument individually. Use the internet, the force is strong with
        #    StackOverflow.
        nregs = self.get_format_count(gadget_format) #generates number of registers in use
        options = self.get_register_combos(nregs, registers) #generates all different combinations
        ret = []
        for i in range (len(options)):
        	ret+= [gadget_format.format(*(options[i]))] #applies a combination of registers on format
        return ret
        #raise NotImplementedError()

    def find_all(self, gadget):
        """
        Return all the addresses of the gadget inside the memory dump.

        Example:
            self.find_all('POP eax')
            => < all ABSOLUTE addresses in memory of 'POP eax; RET' >
        """
        # Notes:
        #
        # 1. Addresses are ABSOLUTE (for example, 0x08403214), NOT RELATIVE to
        #    the beginning of the file (for example, 12).
        #
        # 2. Don't forget to add the 'RET'.
        code = assemble.assemble_data(gadget+"; ret")
        ret = []
        hit = self.dump.find(code,0,len(self.dump))
        while hit!=-1:
        	i = hit+1 #so next search will bypass this
        	ret+=[hit+addresses.LIBC_TEXT_START]
        	hit = self.dump.find(code,i,len(self.dump))
        return ret
        #raise NotImplementedError()

    def find(self, gadget, condition=None):
        """
        Return the first result of find_all. If condition is specified, only
        consider addresses that meet the condition.
        """
        condition = condition or (lambda x: True)
        try:
            return next(addr for addr in self.find_all(gadget)
                        if condition(addr))
        except StopIteration:
            raise ValueError("Couldn't find matching address for " + gadget)

    def find_all_formats(self, gadget_format, registers=GENERAL_REGISTERS):
        """
        Similar to find_all - but return all the addresses of all
        possible gadgets that can be created with this format and registers.
        Every elemnt in the result will be a tuple of the gadget string and
        the address in which it appears.

        Example:
            self.find_all_formats('POP {0}; POP {1}')
            => [('POP eax; POP ebx', address1),
                ('POP ecx; POP esi', address2),
                ...]
        """
        ret = []
        options = self.format_all_gadgets(gadget_format, registers)
        for x in options:
        	tmp =  self.find_all(x)
        	i = 0
        	while i<len(tmp):
        		ret += [(x,tmp[i])]
        		i+=1
        return ret
        #raise NotImplementedError()

    def find_format(self, gadget_format, registers=GENERAL_REGISTERS,
                    condition=None):
        """
        Return the first result of find_all_formats. If condition is specified,
        only consider addresses that meet the condition.
        """
        condition = condition or (lambda x: True)
        try:
            return next(
                addr for addr in self.find_all_formats(gadget_format, registers)
                if condition(addr)
            )
        except StopIteration:
            raise ValueError(
                "Couldn't find matching address for " + gadget_format)

