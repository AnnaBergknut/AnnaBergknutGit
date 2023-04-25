import random


# Abstrakt superklass till alla övergångs klasser
class Transitions():
    def __init__(self):
        self._in_road = None
        self._out_road = None
        self._worker = None
        self._storage = None

# Takes in a _worker from the in road if there is one as well as a _worker available
    def _in_worker(self):
        if self._in_road.unit_availabe() and self._in_road != None:
            self._worker = self._in_road.get_unit()

# Takes out a _worker from the in transition if there is a out road available
    def _out_worker(self):
        if self._out_road != None:
            self._out_road.add_worker(self._worker)
            self._worker = None

# Sets _storage
    def set_storage(self, place):
        self._storage = place

#Sets in road
    def set_in_road(self, _in_road):
        self._in_road = _in_road

# Sets out road
    def set_out_road(self, _out_road):
        self._out_road = _out_road

# Abstrakt metod för implementation i två av fyra specifika klasser
    def produce_unit(self):
        raise NotImplementedError


# Hus klassen, barn klass av övergångar men den som ändrar på mest
class House(Transitions):
    def __init__(self):
        super().__init__()
        self._worker2 = None

# Omdefinierad då i denna klass kan två arbetare behövas tas ut och isåfall behöver man vara specifik med vilken man vill ta bort
    def _out_worker(self, _worker):
        if self._out_road != None and _worker != None:
            self._out_road.add_worker(_worker)
            _worker = None

# Omdefinierad då i denna klass två arbetare behöver ibland tas in
    def _in_worker(self):
        if self._in_road.get_length() > 1:
            self._worker = self._in_road.get_unit()
            self._worker2 = self._in_road.get_unit()

        elif self._in_road.get_length() == 1:
            self._worker = self._in_road.get_unit()

# Producerar en ny arbetare om den kan annars vilar den arbetaren
    def rest_worker(self):
        unit = None
        self._in_worker()
        if self._storage != None and self._storage.unit_availabe() == True:
            unit = self._storage.get_unit()
            if self._worker != None and self._worker2 != None:
                print("Created new worker: True")
                x = Worker()
                self._out_road.add_worker(x)
                unit = None
                self._out_worker(self._worker)
                self._out_worker(self._worker2)
            elif self._worker != None:
                print("Feed worker: True")
                self._worker.set_quality(random.randint(2, 6))
                unit = None
                self._out_worker(self._worker)
            else:
                self._out_worker(self._worker)
                self._out_worker(self._worker2)
                self._storage.add_unit()


# Matsals klassen
class Canteen(Transitions):
    def __init__(self):
        super().__init__()

# Matar arbetaren efter att den har hämtat den
    def feed_worker(self):
        unit = None
        self._in_worker()
        if self._worker != None:
            if self._storage != None and self._storage.unit_availabe() == True:
                unit = self._storage.get_unit()
                self._worker.set_quality(unit.get_quality())
                print("Feed _worker: True")
                self._out_worker()
                unit == None
            else:
                self._out_worker()


# Fabriks klassen
class Factory(Transitions):
    def __init__(self):
        super().__init__()

# Omdefinierad abstrakt metod från superklassen, producerar en ny produkt och lägger in den på lager
    def produce_unit(self):
        self._in_worker()

        if self._worker != None and self._worker.alive() == True:
            print("Produced unit: True")
            self._storage.add_product()
            self._worker.set_quality(-3)
            self._out_worker()


# Omdefinierad abstrakt metod från superklassen, producerar en ny produkt och lägger in den på lager
class Field(Transitions):
    def __init__(self):
        super().__init__()

# Producerar en enhet mat
    def produce_unit(self):
        self._in_worker()
        if self._worker != None and self._worker.alive() == True:
            print("Produced unit: True")
            self._storage.add_food()
            self._worker.set_quality(-3)
            self._out_worker()


# Abstrakta klassen för alla förvarings klasser där unit är ordet för resurser
class Places():
    def __init__(self):
        self._storage = []
        self._in_road = None
        self._out_road = None

# Returnar True om lagret är tomt
    def unit_availabe(self):
        return self._storage != []

# Setter metoder för klassen
    def set_in_road(self, road):
        self._in_road = road

    def set_out_road(self, road):
        self._out_road = road

# Retunerar antal enheter kvar
    def get_length(self):
        return len(self._storage)

# Returnar en unit med kö implementation
    def get_unit(self):
        return self._storage.pop(0)


# Lada klassen som en subklass av platser
class Barn(Places):
    def __init__(self):
        super().__init__()

# Lägger till en enhet mat i lagret
    def add_food(self):
        x = Food()
        self._storage.append(x)


# Fabriks lagret, abstrakt
class Storage(Places):
    def __init__(self):
        super().__init__()

# Lägger till en enhet produkt i lagret
    def add_product(self):
        a = Product()
        self._storage.append(a)

# Omdefinition av get_unit med en stack implementiation, LIFO
    def get_unit(self):
        return self._storage.pop(-1)


# Klassen vägar som en subklass av platser
class Road(Places):
    def __init__(self):
        super().__init__()

# Lägger till en arbetare i _storage
    def add_worker(self, _worker):
        position = 0
        if _worker.alive() and _worker != None:
            self._storage.append(_worker)
            while position < len(self._storage):
                self._storage[position].set_quality(-1)
                if self._storage[position].alive() != True:
                    self._storage.pop(position)
                position = position+1
        else:
            _worker = None

# En metod för att skriva ut arbetarna och hur dessa mår
    def print_workers(self):
        print("Workers in list: ", end="")
        print(len(self._storage))
        print(40*"=")
        for i in range(len(self._storage)):
            print("Current health:", self._storage[i].get_quality(), end="\t")
            print(" Alive:", self._storage[i].alive(), end="\t")
            print(" Place in que:", i+1, end="\t")
            print("Name:", self._storage[i].name)
        print(40*"=")


# En abstrakt klass, implementerad som superklass för resurserna
class Resouces():
    def __init__(self):
        self._quality = None

# Setter funktion för kvaliteten av arbetare och mat
    def set_quality(self, number):
        raise NotImplementedError

# Getter metod för kvaliteten
    def get_quality(self):
        raise NotImplementedError


# En klass för klassens skull, inga metoder att implementera
class Product(Resouces):
    def __init__(self):
        super().__init__()


# Arbetar klassen som en subklass av resurs klassen
class Worker(Resouces):
    def __init__(self):
        super().__init__()
        name_list = ["Brandon", "Alfred", "Steve", "Morales",
                     "Johan", "My", "Rebeca", "Sixten", "Anton"]
        self.name = name_list[random.randint(0, 8)]
        self._quality = 20

# Kollar om arbetaren är vid liv
    def alive(self):
        return self._quality > 0

# Adderar "number" till livet, setter metod
    def set_quality(self, number):
        self._quality = self._quality + number

# Implementerad abstrakt funktion från superklassen
    def get_quality(self):
        return self._quality


# Matklassen
class Food(Resouces):
    def __init__(self):
        super().__init__()
        self._quality = random.randint(5, 10)

# Implementerad abstrakt funktion från superklassen
    def set_quality(self, number):
        self._quality = self._quality + number

# Implementerad abstrakt funktion från superklassen
    def get_quality(self):
        return self._quality


# Huvudprogram
def main():
    r1 = Road()
    f1 = Field()
    s1 = Barn()
    m1 = Canteen()
    f2 = Factory()
    s2 = Storage()
    h1 = House()

    f1.set_in_road(r1)
    f1.set_out_road(r1)
    f1.set_storage(s1)

    f2.set_in_road(r1)
    f2.set_out_road(r1)
    f2.set_storage(s2)

    h1.set_in_road(r1)
    h1.set_out_road(r1)
    h1.set_storage(s2)
    m1.set_storage(s1)
    m1.set_in_road(r1)
    m1.set_out_road(r1)

    for _ in range(4):
        a = Worker()
        r1.add_worker(a)

    q = None
    while r1.unit_availabe() and q != "q":

        print("Currently running: Field")
        f1.produce_unit()
        r1.print_workers()

        print("Currently running: Matsal")
        m1.feed_worker()
        r1.print_workers()

        print("Currently running: Factory")
        f2.produce_unit()
        r1.print_workers()

        print("Currently running: House")
        h1.rest_worker()
        r1.print_workers()
        q = input("Quit? ")

    print(20*"=", "\nDone")


main()
