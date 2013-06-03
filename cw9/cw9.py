##
## interpretacja przykładu użycia wzorca Composite z książki
## "C# 3.0 Design Patterns" wyd. O'Reilly
##
## Program służacy do tworzenia kolekcji zdjęć
## (zamiast obrazów wykorzystujemy ciąg znaków)
##

class flyweight(object):
    """
    Klasa dekorująca
    """
    def __init__(self, cls):
        """
        zmienna _cls przechowuje klasę której elementy mają być tworzone
        
        zmienna _instances jest słownikiem, którego kluczami są parametry
        konstruktora klasy _cls, a wartościami instancje klasy _cls utworzone
        z użyciem tychże parametrów
        """
        self._cls = cls
        self._instances = dict()

    def __call__(self, *args, **kwargs):
        # *args - argumenty pozycyjne zgrupwane postaci krotki
        # **kwargs - argumenty nazwane zgrupowane w postaci słownika
        return self._instances.setdefault(
            (args, tuple(kwargs.items())),
            self._cls(*args, **kwargs))


# Component oraz Composite potrzebują odrębnej implementacji wszystkich metod,
# więc tworzenie wspólnej klasy bazowej powodowałoby zbędny wzrost ilości kodu


# Znaczy to samo co: Component = flyweight(Component)
@flyweight
class Component(object):
    def __init__(self, name):
        self.name = name
        
    def add(self, *args):
        print("Nie można dodać do Component")
        return None

    def remove(self, *args):
        print("Nie można usunąć bezpośrednio")
        return self

    def find(self, name):
        return self if self.name == name else None
    
    def display(self, depth):
        return "-"*depth + self.name + "\n"


class Composite(object):
    def __init__(self, name):
        self.name = name
        self.holder = None
        self.items = []

    def add(self, item):
        self.items.append(item)

    def remove(self, name):
        """
        Usuwa wystąpienie elementu z listy 'items'
        """
        self.items = [i for i in self.items if i.name != name]
        return self

    def find(self, name):
        """
        Wyszukuje element we własnych elementach
        oraz elementach zagnieżdżonych
        """
        if self.name == name:
            return self
        found = None
        for c in self.items:
            found = c.find(name)
            if found is not None:
                break
        return found

    def display(self, depth=0):
        s = "-"*depth
        s += "Set: " + self.name + " length : " + str(len(self.items)) + "\n"
        for item in self.items:
            s += item.display(depth+2)
        return s


class Manager(object):
    """
    Klasa służąca do zarządzania kolekcją zdjęć
    """
    def __init__(self, name):
        self.album = Composite(name)
        self.point = self.album

    def add_set(self, name):
        c = Composite(name)
        self.point.add(c)
        self.point = c

    def add_photo(self, name):
        self.point.add(Component(name))

    def remove(self, name):
        """
        Usuwa element z bieżącego katalogu
        """
        self.point = self.point.remove(name)

    def find(self, name, album=None):
        """
        Wyszukuje "w dół" zaczynająć w folderze przesłanym w drugim parametrze.
        Domyślnie zaczyna wyszukiwanie od folderu głównego
        """
        if album is None:
            self.point = self.album.find(name) or self.point
        else:
            self.point = self.album.find(album) or self.point
            self.point = self.point.find(name)
        return self.point

    def display(self):
        print(self.point.display())


def test():
    manager = Manager("album")
    
    manager.add_set("Home")
    manager.add_photo("Dinner.jpg")
    
    manager.add_set("Pets")
    manager.add_photo("Dog.jpg")
    manager.add_photo("Cat.jpg")

    # powrót do kontenera bazowego
    manager.find("album")

    manager.add_set("Garden")
    manager.add_photo("Spring.jpg")
    manager.add_photo("Summer.jpg")
    manager.add_photo("Flowers.jpg")
    manager.add_photo("Trees.jpg")

    # zawartość "Garden"
    manager.display()

    manager.find("album")
    # zawartość "album"
    manager.display()

    # próba usunięcia obrazu, który nie istnieje w aktualnym kontenerze
    manager.remove("Flowers.jpg")
    manager.display()

    # usunięcie obrazu
    manager.find("Garden")
    manager.remove("Flowers.jpg")
    manager.display()

    # dodanie tego istniejącego obrazu do drugiego kontenera
    manager.find("album")
    manager.add_photo("Summer.jpg")
    manager.display()
    p1 = manager.find("Summer.jpg")
    p2 = manager.find("Summer.jpg", "Garden")

    print("Obraz p1 i p2 są tą samą instancją: ", p1 is p2)
    

if __name__ == "__main__":
    test()
