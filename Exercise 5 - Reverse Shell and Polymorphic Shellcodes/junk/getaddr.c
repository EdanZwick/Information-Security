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
    File * fp;
    struct sockaddr_in serv_addr;
    

    inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr);

    fp = fopen("1.txt","w");
    fwrtite(&serv_addr.sin_addr,4,fp);
    fwrite(fp,'\0');
    fwrite(fp,htons(1337));

    fclose(fp);

}