#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int pid = 0x12345678;
int* adr = (int*) 0x12345678;

int main() {
	int status;
	int is_mayo_inst = 0x00c3c031; /*hex for xor eax, eax ; ret;*/

	if (ptrace(PTRACE_ATTACH, pid, NULL, NULL) == -1) {  // Attach to the process
  		perror("attach");
  		return -1;
	}
	waitpid(pid, &status, 0);  // Wait for the process to stop
	if (WIFEXITED(status)) { return -1; }
	

	if (ptrace(PTRACE_POKETEXT, pid, adr, is_mayo_inst) == -1) {  // Write address
  		perror("write");
  		return -1;
	}

	if (ptrace(PTRACE_DETACH, pid, NULL, NULL) == -1) {  // Detach when done
  		perror("detach");
  		return -1;
	}

    return 0;
}
