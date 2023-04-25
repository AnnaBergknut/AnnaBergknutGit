Mylist = [1,34,56,7,8,94,13,78,90,6]
for i in range(1,len(Mylist)):
    minv = i
    for j in range(i+1,len(Mylist)):
        if Mylist[j] < Mylist[minv]:
            minv = j
        Mylist[i], Mylist[minv] = Mylist[minv], Mylist[i]
print(Mylist)