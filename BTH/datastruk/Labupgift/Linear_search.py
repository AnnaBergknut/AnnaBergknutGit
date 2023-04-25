def search(Mylist, n):
    c = -1
    for i in range(len(Mylist)):
        c += 1
        if Mylist[i] == n:
            print("Found")
            print(f"{n} is on index {c}")
            return True
    return False

Mylist = [1,34,56,7,8,94,13,78,90,6]
n = 13

if search(Mylist, n) == False:
    print("Not Found")
