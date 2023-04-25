# def Mergesort(A):
#     rightindex = len(A)
#     leftindex = 0
#     if len(A) < 2:
#         return A
#     else:
#         middleindex = (leftindex + rightindex) // 2
#         left = Mergesort(A[:middleindex])
#         right = Mergesort(A[middleindex:])
#         merged = Merge(left, right)
#         return merged
        
# def Merge(left, right):
#     result = []
#     i, j = 0, 0

#     while i < len(left) and j < len(right):
#         if left[i] <= right[j] :
#             result.append(left[i])
#             i = i + 1
#         else:
#             result.append(right[j])
#             j = j + 1

#     while i < len(left):
#         result.append(left[i])
#         i = i + 1

#     while j < len(right):
#         result.append(right[j])
#         j = j + 1

#     return result
    
# if __name__ == "__main__":
#     Mylist = [1,34,56,7,8,94,13,78,90,6]
#     sorted = Mergesort(Mylist)
#     print(sorted)
    
def mergesort(lst: list) -> None:
    temp = my_mergesort(lst)
    for i in range(0, len(temp)):
        lst[i] = temp[i]


def my_mergesort(lst) -> None:
    rightindex = len(lst)
    leftindex = 0
    if len(lst) < 2:
        return lst
    else:
        middleindex = (leftindex + rightindex) // 2
        left = my_mergesort(lst[:middleindex])
        right = my_mergesort(lst[middleindex:])
        lst = merge(left, right)
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

if __name__ == "__main__":
    array = [-16,34,56,7,8,94,13,78,90,6,-24, 2,4 ,612,-56, 4, 4, 4, 4, 4]
#     print(quicksort(array), "quicksort")
#     print(insertionsort(array), "insertionsort")
    #print(mergesort(array), "mergesort")
    mergesort(array)
    print(array)
    
#     print(mergesort_hybrid(array), "mergesort_hybrid")
#     print(quicksort_hybrid(array), "quicksort_hybrid")   