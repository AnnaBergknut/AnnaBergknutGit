#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdlib.h>
#include <semaphore.h>
#include <fcntl.h>
#include <pthread.h>

#define SHMSIZE 128
#define SHM_R 0400
#define SHM_W 0200
#define RAND_MAX 2147483647

const char *semName1 = "my_sema1";
const char *semName2 = "my_sema2";

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

	};
	volatile struct shm_struct *shmp = NULL;
	char *addr = NULL;
	pid_t pid = -1;
	int var1 = 0, var2 = 0, shmid = -1;
	struct shmid_ds *shm_buf;

    sem_t *empty = sem_open(semName1, O_CREAT, O_RDWR, 10); //creates a semaphor
	sem_t *full = sem_open(semName2, O_CREAT, O_RDWR, 0);
    int status;

	/* allocate a chunk of shared memory */
	shmid = shmget(IPC_PRIVATE, SHMSIZE, IPC_CREAT | SHM_R | SHM_W);
	shmp = (struct shm_struct *) shmat(shmid, addr, 0);
	shmp->first = 0;
	shmp->last = 0;
	float large;
	float small;
	pid = fork();
	if (pid != 0) { // the parent process will go into this if statment
		large = 0.5; // large and small is fore the float intervall
		small = 0.1;
		/* here's the parent, acting as producer */
		while (var1 < 100) {
			/* write to shmem */

			sem_wait(empty); //lockes
            printf("Sending %d\n", var1); fflush(stdout);
			shmp->buffer[shmp->last++] = var1; // put the var1 valu in the buffer on the first empty space and then move the index

			if (shmp->last == 10) // if the last empty space is over 10 it will become 0 to get the array circular
			{
				shmp->last = 0;
			}
            sem_post(full); // unlockes
			sleep(randFloat(large, small)); //wait a random time
		}
		shmdt(addr);
		shmctl(shmid, IPC_RMID, shm_buf);
        sem_close(full); //closes the semaphor
		sem_close(empty);
		wait(&status);
		sem_unlink(semName1); // unlikes the semaphor from the process
		sem_unlink(semName2);

	} else {
		large = 2;
		small = 0.2;
		/* here's the child, acting as consumer */
		while (var2 < 100) {
			/* read from shmem */
			sem_wait(full);
			var2 = shmp->buffer[shmp->first++]; // putting what was in the first place in the buffer to var2
			if (shmp->first == 10) //if the first val is over 10 it will become 0 to keep the array cirkular
			{
				shmp->first = 0;
			}
			printf("Received %d\n", var2); fflush(stdout);
			sem_post(empty);
            sleep(randFloat(large, small)); // wait a random time
		}
		shmdt(addr);
		shmctl(shmid, IPC_RMID, shm_buf);
        sem_close(empty);
		sem_close(full);
	}
}
