/***************************************************************************
 *
 * Sequential version of Matrix-Matrix multiplication
 *
 ***************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>  
#include <unistd.h>
#include <pthread.h>

#define PROCESSORS 4
#define SIZE 1024

static double a[SIZE][SIZE];
static double b[SIZE][SIZE];
static double c[SIZE][SIZE];


typedef struct threadarg{ // to send the arguments in the right format we put them in a struct
    int first;
    int last;
}threadarg;

void* init_matrix(void* parms)
{
// this function only represents the operation that the threads do in parallel. 
    threadarg *arg = (threadarg*)parms; //copying the arguments to a local struct

    int i, j;

    for (i = arg->first; i < arg->last; i++)
        for (j = 0; j < SIZE; j++) {
	        /* Simple initialization, which enables us to easy check
	         * the correct answer. Each element in c will have the same
	         * value as SIZE after the matmul operation.
	         */
	        a[i][j] = 1.0;
	        b[i][j] = 1.0;
        }
}

void* matmul_seq(void* parms)
{
// this function only represents the operation that the threads do in parallel. 
    threadarg *arg = (threadarg*)parms; //copying the arguments to a local struct

    int i, j, k;

    for (i = arg->first; i < arg->last; i++) {
        for (j = 0; j < SIZE; j++) {
            c[i][j] = 0.0;
            for (k = 0; k < SIZE; k++)
                c[i][j] = c[i][j] + a[i][k] * b[k][j];
        }
    }

}

static void print_matrix(void)
{
    int i, j;

    for (i = 0; i < SIZE; i++) {
        for (j = 0; j < SIZE; j++)
	        printf(" %7.2f", c[i][j]);
	    printf("\n");
    }
}



int main(int argc, char **argv)
{
    time_t begin = time(NULL);

    pthread_t* threads; // declairing a varible to a struct that contains the threads
    threadarg* args; // declairing a varible to a struct that contains the arguments
    threads = malloc(SIZE * sizeof(pthread_t)); //allocate space for thethreads
    args = malloc(SIZE * sizeof(threadarg));
    int rows = SIZE/PROCESSORS; // cauculate how many rows each thread will do
    int i;

    for (i=0; i<PROCESSORS; i++)
    {
        args[i].first = rows*i; // first row
        args[i].last = (i+1)*rows; //last row
        pthread_create(&(threads[i]), NULL, init_matrix, (void*)&args[i]); //create a thread and call init_matrix
    }

    for (i=0; i<PROCESSORS; i++)
    {
        pthread_create(&(threads[i]), NULL, matmul_seq, (void*)&args[i]); //create a thread and call matmul_seq
    }

    for (int p = 0; p < PROCESSORS; p++)
    {
        pthread_join(threads[p], NULL); // join the threads into one
    }
    free(args); // free the memory space
    free(threads);
    


    time_t end = time(NULL);

    printf("%ld\n", (end-begin));
    //print_matrix();
    return 0;
}
