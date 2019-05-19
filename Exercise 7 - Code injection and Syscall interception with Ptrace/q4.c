#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/user.h>

int pid = 0x12345678;

int main(int argc, char **argv) {
    struct user_regs_struct regs;
    int status;

    // Make the malware stop waiting for our output by forking a child process:
    if (fork() != 0) {
        // Kill the parent process so we stop waiting from the malware
        return 0;
    } else {
        // Close the output stream so we stop waiting from the malware
        fclose(stdout);
    }

    // The rest of your code goes here  
    if (ptrace(PTRACE_ATTACH, pid, NULL, NULL) == -1) {  // Attach to the process
        return -1;
    }
    waitpid(pid, &status, 0);  // Wait for the process to stop
    if (WIFEXITED(status)) { return -1; } //if proccess ended, finish

    while(1){
        ptrace(PTRACE_SYSCALL, pid, NULL , NULL); //release until next syscall
        waitpid(pid, &status, 0); //wait for process to stop
        if (WIFEXITED(status)) { return -1; }    
        ptrace(PTRACE_GETREGS, pid, NULL, &regs);
        if (regs.orig_eax == 3){  //check if this syscall is read
            regs.edx = 0;
            ptrace(PTRACE_SETREGS, pid, NULL, &regs);
        }
    }
    return 0;
}