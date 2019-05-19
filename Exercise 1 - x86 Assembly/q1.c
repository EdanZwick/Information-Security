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
    	"CMP EBX, 1;" 
    	"JG _START;" /*if input is 2 or larger we can start looking for primal factors*/
    	"MOV ECX, 0;" /*input is smaller than 2 and has no primal factors, we will return 0*/
    	"JMP _END;"
    	"_START:;"
    	"MOV ECX, EBX;" /*ECX will store candidates to be EBX primal factors since we are looking for the largest we will search top down*/
    	
    	"_LOOP1:;" /*we decrement ECX untill we find a primal number that is also a factor of input*/
    	"MOV EAX, EBX;" /*perlimanery step for division*/
    	"MOV EDX, 0;" /*EDX EAX is now a 64 bit representation of EBX*/
    	"IDIV ECX;" /*Devide the 64 bit representation of EBX with ECX*/
    	"CMP EDX, 0;" /*check if a remainder resaulted*/
    	"JNE _NEXT;" /*ECX is not a coefficiant of EBX move to next iteration*/
 		"MOV ESI, 2;" /*counter for inner loop*/
 		
 		"_LOOP2:;" /*check if ECX is primal by checking if one of the numbers 1 to ECX is it's factor*/
 		"CMP ESI, ECX;" /*did we already go over all numbers smaller than ECX?*/
 		"JE _END;" /*We found a primal!*/ 
 		"MOV EAX, ECX;" /*perlimanery step for division*/
		"MOV EDX, 0;" /*EDX EAX is a 64 bit representation of ECX*/
 		"IDIV ESI;" /*Devide the 64 bit representation of ECX with ESI*/
 		"CMP EDX, 0;" /*check if a remainder resaulted*/
		"JE _NEXT;" /*ECX is not primal, we will keep searching for a primal factor, break out of inner loop and move to outer*/
		"INC ESI;" /*increment inner counter by 1*/
 		"JMP _LOOP2;" /*do another inner loop iteration*/
    	
    	"_NEXT:;" /*do another Outer loop iteration*/
    	"DEC ECX;"
    	"CMP ECX, 2;"
    	"JG _LOOP1;"
    	"_END:;"
    	"MOV EAX, ECX;" /*If we are here, ECX is primal and is a factor of input or 0 if none exist, let's return it*/
        /* Your code stops  here. */
    );

    asm ("MOV %0, EAX"
        : "=r"(output));

    printf("%d\n", output);
    
    return 0;
}