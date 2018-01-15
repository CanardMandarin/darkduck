#include <stdio.h>
#include <string.h> 
#include <sys/socket.h>
#include <stdlib.h> 
#include <errno.h> 
#include <netinet/tcp.h>   
#include <netinet/ip.h> 
#include <netinet/in.h>

struct pseudo_header    //needed for checksum calculation
{
    unsigned int source_address;
    unsigned int dest_address;
    unsigned char placeholder;
    unsigned char protocol;
    unsigned short tcp_length;

    struct tcphdr tcp;
};

BOOL parse_attack(char * attack_str);
unsigned short csum(unsigned short *ptr, int nbytes);
int syn_flood(char *target, uint16_t port, uint32_t count);