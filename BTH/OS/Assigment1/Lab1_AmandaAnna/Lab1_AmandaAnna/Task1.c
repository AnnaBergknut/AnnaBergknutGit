#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main(int argc, char **argv)
{
    pid_t pid;
    unsigned i;
    unsigned niterations = 100;
    pid = fork();
    if (pid == 0) {
        for (i = 0; i < niterations; ++i)
            printf("A = %d, ", i);
     } 
    else {
        printf("child pid: %d\n", pid); //after a fork the parent will be given the childs process id, which is why the parent prints the process id
        pid = fork(); // only the parent will fork again to only get 3 forks
        if (pid == 0)
        {
            for (int i = 0; i < niterations; ++i)
            {
                printf("B = %d, ", i);
            }
        }
        else
        {
            printf("child pid: %d\n", pid); // same as before the parent resives the childes process id
            for (i = 0; i < niterations; ++i)
                printf("C = %d, ", i);
        }
        
        
    }
    printf("\n");
//    printf("%d\n", getpid());

}
