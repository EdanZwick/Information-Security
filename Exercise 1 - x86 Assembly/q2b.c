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
    	"JGE _GO;" /*if the input was greater than 1 we have somthing to work on*/
    	"MOV EAX, 0;"
    	"JMP _END;" /*input was 1 or less, we will return 0*/
    	"_GO:;"
    	"MOV ECX, 0;" /*(i-1)*/
    	"MOV EAX, 1;" /*(i)*/
    	"_LOOP:;"
    	"MOV EDX, ECX;" /*store ECX temporarly*/
    	"MOV ECX, EAX;" /*so ECX will keep (i-1)*/
    	"ADD EAX, EDX;" /*EAX keeps (i)*/
    	"DEC EBX;" /*update counter*/
    	"CMP EBX, 1;" /*did we finish?*/
    	"JG _LOOP;"
    	"_END:;"

        /* Your code stops  here. */
    );

    asm ("MOV %0, EAX"
        : "=r"(output));

    printf("%d\n", output);
    
    return 0;
}
