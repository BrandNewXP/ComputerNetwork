#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <string.h>

#define BLENGTH 1024
#define DPSIZE 2048

typedef struct
{
	int length;
	int seqNumber;
	int ackNumber;
	int fin;
	int syn;
	int ack;
} header;

typedef struct
{
	int data[BLENGTH] ;
	int length;
	int now;
} buffer;

typedef struct
{
	int length;
	int seqNumber;
	int ackNumber;
	int fin;
	int syn;
	int ack;
} header;

void setIP(char *dst, char *src)
{
    if(strcmp(src, "0.0.0.0") == 0 || strcmp(src, "local") == 0 || strcmp(src, "localhost"))
    {
        sscanf("127.0.0.1", "%s", dst);
    }
    else
    {
        sscanf(src, "%s", dst);
    }
}



int main(int argc, char* argv[]){
    int receiversocket, portNum, nBytes, buffer_size;
	char file_path[100] ;
    float loss_rate;
    segment s_tmp;
    struct sockaddr_in sender, agent, receiver, tmp_addr;
    socklen_t sender_size, recv_size, tmp_size;
    char ip[3][50];
    int port[3], i;

    if(argc != 8)
    {
        fprintf(stderr,"用法: %s <sender IP> <agent IP> <sender port> <agent port> <recv port> <file_path> <buffer_size>\n", argv[0]);
		fprintf(stderr, "例如: ./sender local local 8234 8235 8236 text.txt 32\n");
        exit(1);
    }
    else
    {
        setIP(ip[0], argv[1]);
        setIP(ip[1], argv[2]);
        setIP(ip[2], "local");

        sscanf(argv[3], "%d", &port[0]);
        sscanf(argv[4], "%d", &port[1]);
        sscanf(argv[5], "%d", &port[2]);

        sscanf(argv[6], "%s", file_path);
		sscanf(argv[7], "%d", &buffer_size);
    }

    /*Create UDP socket*/
    receiversocket = socket(PF_INET, SOCK_DGRAM, 0);

    /*Configure settings in sender struct*/
    sender.sin_family = AF_INET;
    sender.sin_port = htons(port[0]);
    sender.sin_addr.s_addr = inet_addr(ip[0]);
    memset(sender.sin_zero, '\0', sizeof(sender.sin_zero));

    /*Configure settings in agent struct*/
    agent.sin_family = AF_INET;
    agent.sin_port = htons(port[1]);
    agent.sin_addr.s_addr = inet_addr(ip[1]);
    memset(agent.sin_zero, '\0', sizeof(agent.sin_zero));

    /*bind socket*/
    bind(agentsocket,(struct sockaddr *)&agent,sizeof(agent));

    /*Configure settings in receiver struct*/
    receiver.sin_family = AF_INET;
    receiver.sin_port = htons(port[2]);
    receiver.sin_addr.s_addr = inet_addr(ip[2]);
    memset(receiver.sin_zero, '\0', sizeof(receiver.sin_zero));

    /*Initialize size variable to be used later on*/
    sender_size = sizeof(sender);
    recv_size = sizeof(receiver);
    tmp_size = sizeof(tmp_addr);
	
	/*==============================================================*/
	
	int total_data = 0;
    int drop_data = 0;
    int segment_size, index;
    char ipfrom[1000];
    char *ptr;
    int portfrom;
    srand(time(NULL));
	
	buffer rbuffer ;
	rbuffer.length = buffer_size ;
	rbuffer.now = 0 ;
	
    while(1)
    {
		/*Receive message from agent*/
        memset(&s_tmp, 0, sizeof(s_tmp));
        segment_size = recvfrom(receiversocket, &s_tmp, sizeof(s_tmp), 0, (struct sockaddr *)&tmp_addr, &tmp_size);
        if(segment_size > 0)
        {
            inet_ntop(AF_INET, &tmp_addr.sin_addr.s_addr, ipfrom, sizeof(ipfrom));
            portfrom = ntohs(tmp_addr.sin_port);

            if(strcmp(ipfrom, ip[1]) == 0 && portfrom == port[1])
            {
                /*segment from agent 
                total_data++;*/
                if(s_tmp.head.fin == 1)
                {
                    printf("recv    fin\n");
                    sendto(agentsocket, &s_tmp, segment_size, 0, (struct sockaddr *)&receiver, recv_size);
                    printf("send    finack\n");
					rbuffer.now = 0 ;
					printf("flush\n");
					break ;
                }
				if(s_tmp.head.ack)
                {
                    
                }
                else
                {
                    
                }
            }
			else
			{
				fprintf(stderr, "收到來自 agent 以外的訊息\n");
                exit(1);
			}
		}
	}
	
    return 0;
}
