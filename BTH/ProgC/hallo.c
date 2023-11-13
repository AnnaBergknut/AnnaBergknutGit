#include <stdio.h>
#include <omp.h>

void count_numbers(int thread_num) {
  #pragma omp parallel num_threads()
  {
    int thread_num = omp_get_thread_num();
    #pragma omp for
    for (int i = 0; i < 100; i++) 
    {
      printf("Thread %d counted to %d\n", thread_num, i);
    }
  }   
}

int main() 
{
  int thread_num = 4;
  count_numbers(thread_num);
  return 0;
}