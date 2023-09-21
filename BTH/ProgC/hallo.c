#include <stdio.h>
#include <stdlib.h>


int main()
{

  
    /*
    printf("hallo world \n");
    printf("second test \n");
    */
    /*  
    //int var = 42;
    //int* var_ptr = &var;

    //printf("var = %d\n", var);
    //printf("&var = %p\n", &var);
    //printf("&main = %p\n", &main);
    //printf("varp = %p\n", var_ptr);
    //printf("&varp = %p\n", &var_ptr);
    //printf("*varp = %d\n", *var_ptr);

    //printf("changing var");
    //var = 1234;
    //printf("var = %d\n", var);
    //printf("&var = %p\n", &var);
    //printf("varp = %p\n", var_ptr);
    //printf("&varp = %p\n", &var_ptr);
    //printf("*varp = %d\n", *var_ptr);
    */

    // int* ptr;
    // ptr = malloc(sizeof (int)*2);
    /*char course[] = "DV1580 programing in C";
    char *ptr_to_course = course;

    pritnf("%s\n", &course[10]); // printar från index 10 i course */

    /*
    printf("malptr = %p\n", ptr);
    printf("&malptr = %p\n", &ptr);
    
    printf("malptr = %d\n", ptr[0]);
    printf("*malptr = %d\n", *ptr);


    ptr[0] = 42;
    printf("malptr = %d\n", ptr[0]);
    printf("*malptr = %p\n", *ptr);

    ptr[1] = 22;
    printf("*ptr+1 = %d\n", *(ptr+1));
    printf("malptr = %p\n", ptr);

    printf("\n add\n");
    ptr++;
    printf("malptr = %p\n", ptr);
    printf("&malptr = %p\n", &ptr);
    printf("*malptr = %d\n", *ptr);
    printf("\n minus\n");
    ptr--; // farligt för man kan inte städa efter sig bara framför en
    printf("malptr = %p\n", ptr);
    printf("&malptr = %p\n", &ptr);
    printf("*malptr = %d\n", *ptr);

    free(ptr); */

    return 0;
}

/*
--------------lektion 3---------------
kan vara en bra ide att sätta på gpu acelereringg för vitualbox
foukus på minnet. forstättning nästa vecka. inget på mån

repition enum o strukt
arrayer är pekare som håller addreser. 
----------------------------------------------------------
minne
physiska och virtuella minne.
lång array med hexidesimal addreser
vege addres uplever att de är ensama och har sitt egna omtåde men egentligen är det fragmerat. 

endianness -  har till nätvärk var man skickar grjer. det kan vara olika sakker beroende på hur vi läser det. 
bytes är uppdelade till mest dignifikanta och minst signifikanta. om man nändra på de minsta sig så kommer decimaltalet inte föraändras meddans om man ändrar på de mest sig så kommer numret att förändras mycket

dynamic memory
de sista nyesna uptas av corren. det betyder att den öviga dellen(starten är den dellen av minnet som vi kommer att jobba med
de första bytes lagras text
nästa del är data/static
efter get globla data bss
heap det som vi använder när vi programerar
precis innan coren så använder vi stacken, variaabler som växer på mistat håll.
args är saker vi skickar in ex gcc med fillen
malloc = memory alocation -  hur mcket memory som vi get till variabler. void pekare bt deafult hamlar på heap istället för stack
kom i håg att återlämna minet sennare med free

man kan använda flera pekare för att få flerdimontiella arrayer. 

------------------föreläsning 5-------------------
%s = string
%d = digit
%p = pointer

\n = new row
\t = tab

& = adress till variablem

risker med att programera i ca och vad mǘi gör i minnet
läcka minne med andra ord vi alocerar minne men glömer att ta bort det vilket gör att mycket minne tas up för ingen andledning
buffer overflow. i minnet
- vad händer när man börjar skriva mer minne än vad vi har att använda. vi kan skriva över saker fån annant progrma vilket kan totalt försöra dessa programen. 
  gets_s kan vara en särkare varsion än gets för att man sätter in maxet ridan innan för att stopa buffer overflow

bleading heart  - google
reclusive overflow - google
temp var
figöra ett minne flera gpnger

mmc - googla
när man copierar strängar

valgrind ./a.out
ger mer info

gcc -g codename - googla
----------------------------- f nr:6 --------------------------------------
const
(( don't work
const int nono = 5;
int main (void) 
{
  printf("%d \n ", nono++)
  return 0;
}))

läs från höger till vänster. fungerar meningingen


*/

