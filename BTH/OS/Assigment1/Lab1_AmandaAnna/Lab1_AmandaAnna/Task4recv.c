#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>

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
   int toend;
   key_t key;

   // Generate a key
   if ((key = ftok("msgq.txt", 'B')) == -1) 
   {
      perror("ftok");
      exit(1);
   }
   // Connect to the existing message queue
   if ((msqid = msgget(key, PERMS)) == -1) 
   {
      perror("msgget");
      exit(1);
   }
   printf("message queue: ready to receive messages.\n");

   for(;;) { /* normally receiving never ends but just to make conclusion */
             /* this program ends with string of end */
   
      // Receive a message from the queue
      if (msgrcv(msqid, &buf, sizeof(buf.mtext), 0, 0) == -1) 
      {
         perror("msgrcv");
         exit(1);
      }
      counter == counter++;
      printf("recvd: %d, %d\n", buf.mtext, counter);

      // Break the loop if a termination message is received
      if (buf.mtext == 0)
      {
         break;
      }
   }

   // Cleanup: Remove the file used for key generation
   printf("message queue: done receiving messages.\n");
   system("rm msgq.txt");
   return 0;
}

