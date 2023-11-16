#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdlib.h>
#define SHMSIZE 128
#define SHM_R 0400
#define SHM_W 0200
#define RAND_MAX 2147483647

float randFloat(float large, float small)
{
	//This function returns a random float between two intervalls
    float dif = large - small;
    return (((float) rand() / RAND_MAX) * dif) + small;
}

int main(int argc, char **argv)
{
	struct shm_struct {
		int buffer[10]; // the buffer should at most be able to contain 10 integers
		unsigned char first; // this varible will keep trak on where the first item in the cirkuler array is located
		unsigned char last; // this varible will keep trak on the last item of the circuler array
		unsigned char antal; // this varible will keep track on how many items are in the array
	};
	volatile struct shm_struct *shmp = NULL;
	char *addr = NULL;
	pid_t pid = -1;
	int var1 = 0, var2 = 0, shmid = -1;
	struct shmid_ds *shm_buf;

	/* allocate a chunk of shared memory */
	shmid = shmget(IPC_PRIVATE, SHMSIZE, IPC_CREAT | SHM_R | SHM_W);
	shmp = (struct shm_struct *) shmat(shmid, addr, 0);

	shmp->first = 0;
	shmp->last = 0;
	shmp->antal = 0;
	float large;
	float small;
	pid = fork();
	if (pid != 0) { // the parent process will go into this if statment
		large = 0.5; // large and small is fore the float intervall
		small = 0.1;
		/* here's the parent, acting as producer */
		while (var1 < 100) {
			/* write to shmem */
			var1++;
			while (shmp->antal == 10); /* busy wait until the buffer has space */
			printf("Sending %d\n", var1); fflush(stdout);
			shmp->buffer[shmp->last++] = var1; // put the var1 valu in the buffer on the first empty space and then move the index
			
			shmp->antal++; // showcase that their is one more item in the buffer

			if (shmp->last == 10) // if the last empty space is over 10 it will become 0 to get the array circular
			{
				shmp->last = 0;
			}
			sleep(randFloat(large, small)); //wait a random time
		}
		shmdt(addr);
		shmctl(shmid, IPC_RMID, shm_buf);
	} else {
		large = 2;
		small = 0.2;
		/* here's the child, acting as consumer */
		while (var2 < 100) {
			/* read from shmem */
			while (shmp->antal == 0); /* busy wait until there is something in buffer */
			var2 = shmp->buffer[shmp->first++]; // putting what was in the first place in the buffer to var2
			shmp->antal--; // indecating that an item was removed from the buffer
			if (shmp->first == 10) //if the first val is over 10 it will become 0 to keep the array cirkular
			{
				shmp->first = 0;
			}
			printf("Received %d\n", var2); fflush(stdout);
			sleep(randFloat(large, small)); // wait a random time
		}
		shmdt(addr);
		shmctl(shmid, IPC_RMID, shm_buf);
	}
}
