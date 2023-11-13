#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <unistd.h>
#include <semaphore.h> 

#define SHMSIZE 128
#define SHM_R 0400
#define SHM_W 0200
#define RAND_MAX 2147483647

float RandomBetween(float smallNumber, float bigNumber)
{
    float diff = bigNumber - smallNumber;
    return (((float) rand() / RAND_MAX) * diff) + smallNumber;
}

int main(int argc, char **argv)
{
	struct shm_struct {
		int buffer[10];
		//unsigned empty;
		unsigned char first;
		unsigned char last;
		unsigned char antal;
	};
	volatile struct shm_struct *shmp = NULL;
	char *addr = NULL;
	pid_t pid = -1;
	int var1 = 0, var2 = 0, shmid = -1;
	struct shmid_ds *shm_buf;

	/* allocate a chunk of shared memory */
	shmid = shmget(IPC_PRIVATE, SHMSIZE, IPC_CREAT | SHM_R | SHM_W);
	shmp = (struct shm_struct *) shmat(shmid, addr, 0);
	//shmp->empty = 0;
	shmp->first = 0;
	shmp->last = 0;
	shmp->antal = 0;
	pid = fork();
	if (pid != 0) {
		/* here's the parent, acting as producer */
		while (var1 < 100) {
			/* write to shmem */
			double num = RandomBetween(0.1,0.5);
			sleep(num);
			var1++;
			while (shmp->antal == 10); /* busy wait until the buffer is empty */
			printf("Sending %d\n", var1); fflush(stdout);
			shmp->buffer[shmp->last++] = var1;
			shmp->antal++;

			if (shmp->last == 10)
			{
				shmp->last = 0;
			}
		}
		shmdt(addr);
		shmctl(shmid, IPC_RMID, shm_buf);
	} else {
		/* here's the child, acting as consumer */
		while (var2 < 100) {
			/* read from shmem */
			double num = RandomBetween(0.2,2.0);
			sleep(num);
			while (shmp->antal == 0); /* busy wait until there is something */
			var2 = shmp->buffer[shmp->first++];
			shmp->antal--;
			if (shmp->first == 10)
			{
				shmp->first = 0;
			}
			printf("Received %d\n", var2); fflush(stdout);
		}
		shmdt(addr);
		shmctl(shmid, IPC_RMID, shm_buf);
	}
}
