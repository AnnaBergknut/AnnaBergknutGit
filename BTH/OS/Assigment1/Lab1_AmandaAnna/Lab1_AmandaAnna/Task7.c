#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

struct threadArgs 
{
    unsigned int id;
    unsigned int numThreads;
    int squaredId;
};

// Define a counter and a mutex for synchronization
unsigned int counter = 0;
pthread_mutex_t counterMutex = PTHREAD_MUTEX_INITIALIZER;

void* child(void* params) 
{ //
    struct threadArgs *args = (struct threadArgs*) params;
    unsigned int childID = args->id;
    unsigned int numThreads = args->numThreads;

    // Calculate the squared ID
    args->squaredId = childID * childID;

    printf("Greetings from child #%u of %u. Squared ID: %d\n", childID, numThreads, args->squaredId);

    // Exit the thread and pass the squared ID back to the parent
    pthread_exit(NULL);
}

int main(int argc, char** argv) 
{
    pthread_t* children; // dynamic array of child threads
    struct threadArgs* args; // argument buffer
    unsigned int numThreads = 8;

    // If an argument is provided, it's converted to an integer using atoi and assigned to numThreads.
    if (argc > 1)
    {
        numThreads = atoi(argv[1]);
    }
    children = malloc(numThreads * sizeof(pthread_t)); // allocate array of handles
    args = malloc(numThreads * sizeof(struct threadArgs)); // args vector

    for (unsigned int id = 0; id < numThreads; id++) 
    {
        // create threads
        args[id].id = id;
        args[id].numThreads = numThreads;
        args[id].squaredId = 0;
        pthread_create(&(children[id]), NULL, child, (void*)&args[id]);
    }
   

    // Print the squared IDs received from each child thread
    for (int id = 0; id < numThreads; id++) 
    {
        pthread_join(children[id], NULL);
    }
    printf("I am the parent (main) thread.\n");
    for (int id = 0; id < numThreads; id++)
    {
        printf("Squared ID received from child #%u: %d\n", id, args[id].squaredId);
    }

    // Cleanup
    free(args); // deallocate args vector
    free(children); // deallocate array
    return 0;
}