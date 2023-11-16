#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>
#include <termios.h>
#include <fcntl.h>

#define numThreads 5

pthread_mutex_t chopstick[numThreads]; //Creates the chopsticks and set them to mutex objekts
volatile int programRunning = 1;  // Flag to indicate if the program is running

void thinking(int professorId) 
{
    printf("Professor %d is thinking...\n", professorId);
    sleep(rand() % 5 + 1);
    return;
}

void leftChopstick(int professorId) 
{
    int leftChopstickId = professorId;

    if (pthread_mutex_trylock(&chopstick[leftChopstickId]) == 0) {
        printf("Professor %d got left chopstick and is thinking...\n", professorId);
        sleep(rand() % 8 + 2);
    } else 
    {
        printf("Professor %d didn't have a chopstick on the left\n", professorId);
        printf("Professor %d is thinking...\n", professorId);
        thinking(professorId);
        if (pthread_mutex_trylock(&chopstick[leftChopstickId]) == 0) 
        {
            printf("Professor %d  try again and got the left chopstick\n", professorId);
        }else
        {
            pthread_mutex_unlock(&chopstick[leftChopstickId]);
        } 
    }
}

void rightChopstick(int professorId) 
{
    int rightChopstickId = (professorId + 1) % numThreads;

    if (pthread_mutex_trylock(&chopstick[rightChopstickId]) == 0) 
    {
        printf("Professor %d got right chopstick\n", professorId);
    } else 
    {
        printf("Professor %d didn't have a chopstick on the right\n", professorId);
        printf("Professor %d is thinking...\n", professorId);
        thinking(professorId);
        if (pthread_mutex_trylock(&chopstick[rightChopstickId]) == 0) 
        {
            printf("Professor %d  try again and got the right chopstick\n", professorId);
        }else
        {
            pthread_mutex_unlock(&chopstick[rightChopstickId]);
        }      
    }
}

void eating(int professorId) 
{
    int leftChopstickId = professorId;
    int rightChopstickId = (professorId + 1) % numThreads;

    // Check if both chopsticks are acquired
    if (pthread_mutex_trylock(&chopstick[leftChopstickId]) == 0 &&
        pthread_mutex_trylock(&chopstick[rightChopstickId]) == 0) 
    {
        printf("Professor %d is eating\n", professorId);
        sleep(rand() % 10 + 5);

        // Release both chopsticks after eating
        pthread_mutex_unlock(&chopstick[leftChopstickId]);
        pthread_mutex_unlock(&chopstick[rightChopstickId]);
    }
}

void *inputListener(void *arg) // Found on the internet
{
    int ch;
    struct termios oldt, newt;

    // Set terminal to non-blocking mode
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    int flags = fcntl(STDIN_FILENO, F_GETFL, 0);
    fcntl(STDIN_FILENO, F_SETFL, flags | O_NONBLOCK);

    while (programRunning) 
    {
        ch = getchar();
        if (ch == 27) {  // Check for ESC key
            programRunning = 0;
            break;
        }
    }

    // Restore terminal settings
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    fcntl(STDIN_FILENO, F_SETFL, flags);

    return NULL;
}

void *diningProfessor(void *arg) 
{
    int professorId = *((int *)arg);

    while (programRunning) 
    {
        thinking(professorId);
        leftChopstick(professorId);
        rightChopstick(professorId);
        eating(professorId);
    }

    return NULL;
}

int main() 
{
    srand(time(NULL)); // seed the random number generator

    pthread_t professors[numThreads];
    pthread_t inputThread;
    int professorIds[numThreads];

    // Initialize mutex locks for chopsticks
    for (int i = 0; i < numThreads; i++) 
    {
        pthread_mutex_init(&chopstick[i], NULL);
    }

    // Create professor threads
    for (int i = 0; i < numThreads; i++) 
    {
        professorIds[i] = i;
        pthread_create(&professors[i], NULL, diningProfessor, (void *)&professorIds[i]);
    }

    // Create input listener thread
    pthread_create(&inputThread, NULL, inputListener, NULL);

    // Wait for input thread to finish
    pthread_join(inputThread, NULL);

    // Stop professor threads
    programRunning = 0;
    printf("ESC key pressed \n");

    // Wait for professor threads to finish
    for (int i = 0; i < numThreads; i++) 
    {
        pthread_join(professors[i], NULL);
    }

    // Cleanup
    for (int i = 0; i < numThreads; i++) 
    {
        pthread_mutex_destroy(&chopstick[i]);
    }

    printf("Ending program \n");
    return 0;
}
