#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <unistd.h>

#define PERMS 0644
struct my_msgbuf 
{
   long int mtype;
   int mtext;
};

int main(void) 
{
   int counter = 0; 
   struct my_msgbuf buf;
   int msqid;
   int len;
   key_t key;
   system("touch msgq.txt");

   // Generate a key 
   if ((key = ftok("msgq.txt", 'B')) == -1) //Check if ftok was successful by comparing the result to -1. If ftok fails, print an error message using perror.
   {
      perror("ftok");
      exit(1);
   }

   // Create or connect to a message queue
   if ((msqid = msgget(key, PERMS | IPC_CREAT)) == -1) 
   {
      perror("msgget");
      exit(1);
   }
   printf("message queue: ready to send messages.\n");
   buf.mtype = 1; /* we don't really care in this case */

   char first[20];
   int tostart;

   // Wait for user input to start sending messages
   while(1)
   {
      printf("Are we ready?\n");
      fgets(first, sizeof first, stdin);
      len = strlen(first);
      if (first[len-1] == '\n') first[len-1] = '\0';
      tostart = strcmp(first,"ready");
      if (tostart == 0)
         break;
   }
   len = 4;

   // Send 50 messages to the message queue
   for (int i = 0; i < 50; i++)
   {
      counter = ++counter;
      buf.mtext = rand();
      buf.mtext = (rand() % 2147483647) + 1; 
      printf("%d, %d\n", buf.mtext, counter);

      // Send the message to the queue
      if (msgsnd(msqid, &buf, len, 0) == -1) /* +1 for '\0' */
         perror("msgsnd");
   }

   // Send a termination message to signal the end
   buf.mtext = 0;
   if (msgsnd(msqid, &buf, len, 0) == -1) /* +1 for '\0' */
   {
      perror("msgsnd");
   }

   // Allow some time for the receiver to process messages
   sleep(10);

   // Remove the message queue
   if (msgctl(msqid, IPC_RMID, NULL) == -1) 
   {
      perror("msgctl");
      exit(1);
   }

   printf("message queue: done sending messages.\n");
   return 0;
}
