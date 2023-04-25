Mylist = [1,2,4,5,6,8,9,16,29,35,48,77,100]
n = 48

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