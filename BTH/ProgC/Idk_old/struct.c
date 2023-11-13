#include <stdio.h>
#include <string.h>

struct Person 
{
  char name[50];
  int citNo;
  float salary;
} person1;

struct Ppl 
{
  char name[50];
  int citNo;
  float salary;
} ppl2;

int main() 
{
  strcpy(person1.name, "George Orwell");
  person1.citNo = 1984;
  person1. salary = 2500;

  strcpy(person1.name, "Peter kemp");
  person1.citNo = 1972;
  person1. salary = 2250;

  printf("Name: %s\n", person1.name);
  printf("Citizenship No.: %d\n", person1.citNo);
  printf("Salary: %.2f\n", person1.salary);
  /*printf("Name: %s\n", ppl2.name);
  printf("Citizenship No.: %d\n", ppl2.citNo);
  printf("Salary: %.2f\n", ppl2.salary);*/

  return 0;
}