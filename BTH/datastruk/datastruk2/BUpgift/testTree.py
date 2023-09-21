import math

quick = [2.956e-05, 3.890e-04, 4.355e-3, 5.436e-2, 0.648 ]
merge = [6.988e-05, 7.038e-04, 8.977e-3, 9.560e-2, 1.130 ]
number = 10
print("----- Quicksort C -----")
for i in quick:
    constant = i / number * math.log2(number)
    print("quick", number, constant)
    number = number*10
number = 10 
print("----- Mergesort C -----")  
for i in merge:
    constant = i / number * math.log2(number)
    print("merge", number, constant)
    number = number*10
