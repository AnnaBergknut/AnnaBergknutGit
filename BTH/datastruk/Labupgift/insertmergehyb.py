import sys
import time
from pathlib import Path
import numpy as np

def insertionsort(lst:list) -> None:
    """ insertionsort """
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
    """ merge hyb """
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

def main():
    print("------------------------------------------------------------------")
    input_list = np.random.randint(1, 100, size=20).tolist()
    print(input_list, "111111111111")
    mergesort_hybrid(input_list)
    print(input_list, "2222222222222222")
    # for i in range(0,5):
    #     input_list = np.random.randint(1000, 999999, size=20).tolist()
    #     timestamp_before = time.perf_counter()
    #     mergesort_hybrid(input_list)
    #     timestamp_after = time.perf_counter()
    #     runtime = timestamp_after - timestamp_before
    #     print(runtime)

if __name__ == "__main__":
    main()