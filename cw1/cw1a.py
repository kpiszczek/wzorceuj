"""wersja 1 - sigleton "funkcyjny" """
"""Definicja dekoratora przechowującego, którego kluczami
są klasy a wartościami odpowiadające im instancje"""
def singleton(cls):
    instances = dict()
    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance

"""Dzięki dekoratorowi możemy utworzyć tylko jedną instancję tej klasy.
W tym momencie dana klasa przestaje być klasą, a staję się funkcją
>>>type(TestClass)
<type 'function'>
Próba utworzenia podklasy zakończy się błędem
>>>class SubClass(TestClass):
    pass
...
TypeError: Error when calling the metaclass bases
    function() argument 1 must be code, not str"""
@singleton
class TestClass:
    def __init__(self):
        self.counter = 0
    def increment_counter(self):
        self.counter += 1
"""==================================================================="""

"""wersja 2 - klasa bazowa"""
class Singleton(object):
    # zmienna statyczna
    _instance = None
    def __new__(cls,*args,**kwargs):
        if not isinstance(cls._instance,cls):
            cls._instance = object.__new__(cls,*args,**kwargs)
        return cls._instance
    # metoda statyczna
    @classmethod
    def get_instnace(cls):
        return cls._instance
    
class TestClass2(Singleton):
    def __init__(self):
        # zmienna lokalna/instancji klasy
        self.counter = 0
    def increment_counter(self):
        self.counter += 1

"""==================================================================="""

"""wersja 3"""
"""Bezpośrednia implementacja funkcjonalności sigletonu wewnątrz klasy.
Ze względu na brak możliwości ukrycia konstruktora w języku Python przy
próbie jego powtórnego wywołania zostanie wyrzucony wyjątek (w poprzednich
przypadkach została zwracana ta sama instancja klasy)"""
class MultipleSingletonInstanceError(Exception):
    pass

class TestClass3:
    _instance = None
    def __init__(self):
        self.counter = 0
        if TestClass3._instance is not None:
            raise MultipleSingletonInstanceError
        TestClass3._instance = self
    @staticmethod
    def get_instance(self):
        return _instance
    def increment_counter(self):
        self.counter += 1

"""funkcja testująca zdefiniowane klasy"""
def test(cls): 
    o1 = cls()
    o2 = cls()
    print(o1 is o2)
    o1.increment_counter()
    print(o1.counter)
    o2.increment_counter()
    print(o2.counter)

if __name__ == "__main__":
    test(TestClass)
    test(TestClass2)
    try:
        test(TestClass3)
    except MultipleSingletonInstanceError:
        print("Nie można stworzyć drugiej instancji singletona!")
    
