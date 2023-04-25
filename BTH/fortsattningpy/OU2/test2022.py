import random
from collections import deque
#------- randome numbers ----------------------------------------------------------------------------------
# number = random.randint(1,6)
# print(number)
# dice = 5   
# diceList = [] 
# for i in range(dice):
#     diceList.append(f"d{i+1}")
#     print(i)
    
# print(diceList)

#------- mängdlära -----------------------------------------------------------------------------------
# x = set([4, 2, 9, 3, 1])
# y = set([5, 4, 8])

# a = x.union(y)
# b = x.difference(y)
# c = x.intersection(y)

# print(a)
# print(b)
# print(c)

#----- que ----------------------------------------------------------------------------
# class Queue:
    
#     def __init__(self):
#         self._values = deque([]) # Skapar en tom lista

#     def enqueue(self, value):
#         for i in  value:
#             self._values.append(i) # Lägger till ett värde till höger (sist) i listan
#         print(self._values)

#     def dequeue(self):
#         assert(len(self._values) > 0)
#         return self._values.pop(0) # Tar bort och returnerar värdet till vänster (först) i listan.

#     def front(self):
#         assert(len(self._values) > 0)
#         return self._values[0] # Returnerar första värdet i listan

#     def __len__(self): # Gör att vi kan använda len-funktionen på kö-objektet
#         return len(self._values) 

#     def __str__(self): #Gör att vi kan få en strängrepresentation av kön.
#         return str(self._values)
    
# if __name__ == "__main__":
#     value = [1, 2, 3, 3, 4, 2, 4]
#     room = Queue()
#     room.enqueue(value) 
    
#---------------------------------------------------------------------------------


