
def insertionsort(my_array):
    for i in range(1, len(my_array)):
        number = my_array[i]
        j = i
        while j > 0 and my_array[j - 1] > number:
            my_array[j] = my_array[j - 1]
            j = j - 1
        my_array[j] = number
 
if __name__ == '__main__':
 
    array = [1,34,56,7,8,94,13,78,90,6]
    print( array, "insertionsort")

