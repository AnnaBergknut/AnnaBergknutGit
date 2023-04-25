"""
Written by Anna Bergknut, October 2022
"""

import sys
import time
from pathlib import Path
import numpy as np

version = sys.version_info
if version[0] < 3 :
    print(f'Please install python 3, at least version 3.6. You have {version[0]}.{version[1]}.')
    sys.exit(1)
elif version[1] < 6:
    print(f'Please install python 3, at least version 3.6. You have {version[0]}.{version[1]}.')
    sys.exit(1)

def quicksort(lst: list) -> None: 
    """ Quicksort uses a divide and conquer method by dividing the list in to two lists based if it is bigger or smaller the the pivot. With an average speed of O(nlog {n})  """
    low = 0
    high = len(lst)-1
    my_quicksort(lst, low, high)

def my_quicksort(lst, low, high):
    if low<high:
        pivot = partition(lst, low, high)
        my_quicksort(lst, low, pivot-1)
        my_quicksort(lst, pivot + 1, high)
        return lst

def partition(lst, low, high):
    """ Decide the pivot and ruffly sort in two lists """
    pivot = lst[high]
    i = j = low
    for i in range(low, high):
        if lst[i]<pivot:
            lst[i], lst[j] = lst[j], lst[i]
            j+= 1
    lst[j], lst[high] = lst[high], lst[j]
    return j

def insertionsort(lst:list) -> None:
    """ Insertionsort assume that the first element is sorted and then insert the next elements on a sorted spot. With an average speed of O( n^2) """
    low = 0
    high = len(lst)-1
    my_insertionsort(lst, low, high)

def my_insertionsort(lst, low, high):
    for i in range(low + 1, high + 1):
        number = lst[i]
        j = i
        while j>low and lst[j-1]>number:
            lst[j]= lst[j-1]
            j-= 1
        lst[j]= number       
    return lst

def mergesort(lst:list) -> None:
    """ Mergesort is a divide and conquer algorithm that divide until we have only lonely elements and then merge dem sorted.. With an average speed of O(nlog {n}) """
    temp = my_mergesort(lst)
    for i in range(0, len(temp)):
        lst[i] = temp[i]      

def my_mergesort(lst:list):
    rightindex = len(lst)
    leftindex = 0
    if rightindex < 2:
        return lst
    else:
        middleindex = (leftindex + rightindex) // 2
        left = my_mergesort(lst[:middleindex])
        right = my_mergesort(lst[middleindex:])
        merged = merge(left, right)
        return merged       

def merge(left, right):
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j] :
            result.append(left[i])
            i = i + 1
        else:
            result.append(right[j])
            j = j + 1
    while i < len(left):
        result.append(left[i])
        i = i + 1
    while j < len(right):
        result.append(right[j])
        j = j + 1
    return result

def mergesort_hybrid(lst:list) -> None:
    """ Mergesort and insertionsort hybrid. Ones mergesort have divided the data in to smaller lists of less then 10 the insertion sort will sort it because that is a lot faster. """
    temp = my_mergesort_hybrid(lst)
    for i in range(0, len(temp)):
        lst[i] = temp[i]

def my_mergesort_hybrid(lst:list):
    low = 0
    high = len(lst)
    if high-low + 1 < 10:
        high = high -1
        temp = my_insertionsort(lst, low, high)
        high = high +1
        return temp
    elif low < high:
        mid = ((low+high)//2)
        left = my_mergesort_hybrid(lst[low:mid])
        right = my_mergesort_hybrid(lst[mid:high])
        merged = merge(left, right)
        return merged

def quicksort_hybrid(lst: list) -> None:
    """ Quicksort and insertionsort hybrid. Ones quicksoert have divided the data in to smaller lists of less then 10 the insertionsort will sort it because that is a lot faster. """
    low = 0
    high = len(lst)-1
    my_quicksort_hybrid(lst, low, high)
    
def my_quicksort_hybrid(lst, low, high):
    while low<high:

        if high-low + 1 < 10:
            my_insertionsort(lst, low, high)
            break
 
        else:
            pivot = partition(lst, low, high)

            if pivot-low<high-pivot:
                my_quicksort_hybrid(lst, low, pivot-1)
                low = pivot + 1
            else:
                my_quicksort_hybrid(lst, pivot + 1, high)
                high = pivot-1
    return lst

def main():
    """ I have used main in other to test runtime but in this instance this script functions is getting called from tests.py which means that this will never get used. """
    avg = 0
    for i in range(0,5):
        input_list = np.random.randint(1000, 999999, size=100000).tolist()
        timestamp_before = time.perf_counter()
        mergesort_hybrid(input_list)
        timestamp_after = time.perf_counter()
        runtime = timestamp_after - timestamp_before
        print(runtime)
        avg = avg + runtime
    print(f"avg {avg/5}")

if __name__ == "__main__":
    main()
   