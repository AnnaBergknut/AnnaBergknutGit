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


#define SIZE 1024

static double a[SIZE][SIZE];
static double b[SIZE][SIZE];
static double c[SIZE][SIZE];

typedef struct threadarg{ // to send the arguments in the right format we put them in a struct
    int row;
}threadarg;

void* fill(void* parm)
{
    // this function only represents the operation that the threads do in parallell
    threadarg *arg = (threadarg*)parm; ///copying the arguments to a local struct
    int j, k;
    int row = arg->row; //accesing the argument from struct
    for (j = 0; j < SIZE; j++) 
    {
        /* Simple initialization, which enables us to easy check
            * the correct answer. Each element in c will have the same
            * value as SIZE after the matmul operation.
            */
        a[row][j] = 1.0;
        b[row][j] = 1.0;
    }

}

static void init_matrix(void)
{
    pthread_t* threads; // declairing a varible to a struct that contains the threads
    threadarg* args; // declairing a varible to a struct that contains the arguments
    threads = malloc(SIZE * sizeof(pthread_t)); //allocate space for thethreads
    args = malloc(SIZE * sizeof(threadarg));
    int i;


    for (i = 0; i < SIZE; i++)
    {
        args[i].row = i; // put the argument into the argument struct
        pthread_create(&(threads[i]), NULL, fill, (void*)&args[i]); //create a thread and call fill
    }

    for (int p = 0; p < SIZE; p++)
        pthread_join(threads[p], NULL); // join the threads into one

    free(args);  // free the memory space
    free(threads);
}

void* mult(void* parms)
{
    // this function only represents the operation that the threads do in parallel. 
    threadarg *arg = (threadarg*)parms; //copying the arguments to a local struct
    int j, k;
    int row = arg->row; //accesing the argument from struct
    for (j = 0; j < SIZE; j++) 
    {
        c[row][j] = 0.0;
        for (k = 0; k < SIZE; k++)
            c[row][j] = c[row][j] + a[row][k] * b[k][j];
    }
}

static void matmul_seq()
{
    pthread_t* threads; // declairing a varible to a struct that contains the threads
    threadarg* args; // declairing a varible to a struct that contains the arguments
    threads = malloc(SIZE * sizeof(pthread_t)); //allocate space for thethreads
    args = malloc(SIZE * sizeof(threadarg));

    int i, j, k;
    for (i = 0; i < SIZE; i++) 
    {
        args[i].row = i; // put the argument into the argument struct
        pthread_create(&(threads[i]), NULL, mult, (void*)&args[i]); //create a thread and call mult
    }
    for (int p = 0; p < SIZE; p++)
        pthread_join(threads[p], NULL); // join the threads into one

    free(args); // free the memory space
    free(threads);
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
 

    init_matrix();
    matmul_seq();


    time_t end = time(NULL);

    printf("%ld\n", (end-begin));
    //print_matrix();
    return 0;
}
