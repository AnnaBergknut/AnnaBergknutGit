
def insort(Mylist):
    for i in range(1,len(Mylist)):
        j = i-1
        temp = Mylist[i]
        while j >= 0 and temp < Mylist[j] :
            Mylist[j + 1] = Mylist[j]
            j -= 1
        Mylist[j + 1] = temp  
    return Mylist

def binosearch(Mylist):
    high = len(Mylist) -1
    low = 0
    mid = 0
    run = True
    while low <= high and run:
        mid = (high + low)// 2
        if Mylist[mid] == n:
            print(f"on index {mid} we found {n}")
            run = False
        elif Mylist[mid] > n:
            high = mid -1
        elif Mylist[mid] < n:
            low = mid + 1
        else:
            print("Not Found")
        
if __name__ == "__main__":
    Mylist = [1,34,56,7,8,94,13,78,90,6,249,1234556678,1075,7592,5778295,182151,9076,46532447,0,6,2,6754]
    n = 94

    sorted =insort(Mylist)
    binosearch(sorted)