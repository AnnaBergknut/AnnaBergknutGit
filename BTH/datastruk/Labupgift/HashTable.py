""" HashTable """
class HashTable():
    def __init__ (self):
        self.hashTable = [[],] * 11
        self.testarry  = []

    def add(self, index):
        if self.hashTable[index] == []:
            self.hashTable[index] = number
        else:
            print(f"we had a colition on {index} we should have a funktion where we choice what colition method we will do")
        print(self.hashTable)

    def find():
        pass

    def delete():
        pass

    def hash(self, number):
        m = len(self.hashTable)
        print(self.hashTable)
        index = number % m
        
        
            

if __name__ == "__main__":
    room = HashTable()
    testarray  = [83, 77, 65, 17, 9, 31,6]
    m = 11
    # hashTable = [[],] * m
    for i in testarray:
        room.hash(i)
        
    # print(hashTable)
