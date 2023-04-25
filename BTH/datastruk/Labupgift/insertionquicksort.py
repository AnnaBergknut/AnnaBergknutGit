def insertion_sort(my_array, low, high):
    for i in range(low + 1, high + 1):
        number = my_array[i]
        j = i
        while j>low and my_array[j-1]>number:
            my_array[j]= my_array[j-1]
            j-= 1
        my_array[j]= number
        
    return my_array
 
# The following two functions are used
# to perform quicksort on the array.
 
# Partition function for quicksort
def partition(my_array, low, high):
    pivot = my_array[high]
    i = j = low
    for i in range(low, high):
        if my_array[i]<pivot:
            array[i], array[j]= array[j], array[i]
            j+= 1
    array[j], array[high]= array[high], array[j]
    return j
 
# Function to call the partition function
# and perform quick sort on the array
def quick_sort(my_array, low, high):
    if low<high:
        pivot = partition(my_array, low, high)
        quick_sort(my_array, low, pivot-1)
        quick_sort(my_array, pivot + 1, high)
        return my_array
 
# Hybrid function -> Quick + Insertion sort
def hybrid_quick_sort(my_array, low, high):
    while low<high:
 
        # If the size of the array is less
        # than threshold apply insertion sort
        # and stop recursion
        if high-low + 1 < high//2:
            insertion_sort(my_array, low, high)
            break
 
        else:
            pivot = partition(my_array, low, high)
 
            # Optimised quicksort which works on
            # the smaller arrays first
 
            # If the left side of the pivot
            # is less than right, sort left part
            # and move to the right part of the array
            if pivot-low<high-pivot:
                hybrid_quick_sort(my_array, low, pivot-1)
                low = pivot + 1
            else:
                # If the right side of pivot is less
                # than left, sort right side and
                # move to the left side
                hybrid_quick_sort(my_array, pivot + 1, high)
                high = pivot-1
 
# Driver code
 
array = [ 24, 97, 40, 67, 88, 85, 15,
      66, 53, 44, 26, 48, 16, 52,
      45, 23, 90, 18, 49, 80, 23 ]
hybrid_quick_sort(array, 0, len(array)-1)
print(array)