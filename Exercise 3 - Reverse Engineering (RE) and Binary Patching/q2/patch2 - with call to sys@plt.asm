mov		EAX , 0x08048662 
jmp	    EAX #skip this part first time around
mov		AX , word ptr[EBP-0x40C] #check 2 first bytes for shabang
test	AL , 0x23
jz		skip
test	AH , 0x21
jz		skip


lea     eax , [EBP-0x40C] #this is the pointer to file contents, load to eax for syscall
push	eax

call	0x8047E93	 #call system, creating seg fault
#jmp skip

pop		eax

mov		EAX , 0x08048659
jmp		EAX
skip: #if not equal to shabang we will go back to running normal code
pop		EAX #bring back stack to normal condition
mov		EAX , 0x0804863A 
jmp		EAX
