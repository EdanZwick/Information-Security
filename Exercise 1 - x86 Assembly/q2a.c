#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
    int input, output;

    if (argc != 2) {
        printf("USAGE: %s <number>\n", argv[0]);
        return -1;
    }

    input = atoi(argv[1]);

    asm ("MOV EBX, %0"
        :
        : "r"(input));

    asm (
        /* Your code starts here. */
    	/*Since I know i push exactly 2 ints to the stack each iteration, I don't keep the ESP on the stack but just decrement it manually each time a recursion folds*/
    	"CMP EBX, 0;"
    	"JG _GO;" /*if the input was greater than 0 we have somthing to work on*/
    	"MOV EAX, 0;"
    	"JMP _END;" /*input was 0 or less, we will return 0*/
    	"_GO:;" 
    	"PUSH 0;" /*push initial values of the sequence*/
    	"PUSH 1;"
    	"CALL _FIBO;"
    	/*Since I know i push exactly 2 ints to the stack each iteration, I don't keep the ESP on the stack but just decrement it manually each time a recursion folds*/
    	"ADD ESP,8;" /*restore stack*/
    	"JMP _END;" /*Since this is where we will return to after recurtion ends*/
    	
    	"_FIBO:;"
    	"MOV ECX, DWORD PTR [ESP+8];" /*get a(i-2)*/
    	"MOV EDX, DWORD PTR [ESP+4];" /*get a(i-1)*/
    	"ADD ECX, EDX;" /*calculate a(i)*/
		"CMP EBX, 2;" /*is this the final value to calculate?*/
    	"JG _CONT;"
    	"MOV EAX, ECX;" /*this is the droid we are looking for*/
    	"RET;" /*NO need to keep runing- start folding recursion*/
    	"_CONT:;" /*There are more cycles to preform*/
    	"PUSH EDX;" /*store a(i-1)*/
    	"PUSH ECX;" /*store a(i-2)*/
    	"DEC EBX;" /*decrement 1 from the number of cycles left to preform*/
    	"CALL _FIBO;" /*recursivly call the function to calculate the sequence*/
    	"ADD ESP,8;" /*restore the stack to the way we recieved it*/
    	"RET;"

    	"_END:;"
    	
        /* Your code stops  here. */
    );

    asm ("MOV %0, EAX"
        : "=r"(output));

    printf("%d\n", output);
    
    return 0;
}
