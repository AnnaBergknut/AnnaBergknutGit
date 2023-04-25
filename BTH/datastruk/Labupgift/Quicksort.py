
def QuickSort(my_array):

    elements = len(my_array)
    
    #Base case
    if elements < 2:
        return my_array
    
    current_position = 0 #Position of the partitioning element

    for i in range(1, elements): #Partitioning loop
         if my_array[i] <= my_array[0]:
              current_position += 1
              temp = my_array[i]
              my_array[i] = my_array[current_position]
              my_array[current_position] = temp

    temp = my_array[0]
    my_array[0] = my_array[current_position] 
    my_array[current_position] = temp #Brings pivot to it's appropriate position
    
    left = QuickSort(my_array[0:current_position]) #Sorts the elements to the left of pivot
    right = QuickSort(my_array[current_position+1:elements]) #sorts the elements to the right of pivot

    my_array = left + [my_array[current_position]] + right #Merging everything together
    
    return my_array    

if __name__ == "__main__":
    array = [1,34,56,7,8,94,13,78,90,6]
    print(QuickSort(array))