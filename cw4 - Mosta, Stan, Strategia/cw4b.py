"""
Treść zadania:

Wybierz 3 algorytmy sortowania (na przykład sortujące
tablice liczb). Stworz odpowiadające im trzy klasy implementujące te
algorytmy oraz abstrakcyjna klase nadrzedna definiujaca tylko interface.
Pokaz przykład uzycia takiej ‘konstrukcji’.
"""


import types
from copy import copy
from random import randrange, randint

# Ze względu na dynamiczną naturę języka Python nie ma konieczności
# tworzenie klas strategii konkretnych. Zamiast tego można dynamicznie
# zmienić (przypisać) metodę do istniejącego obiektu

class Sorter(object):
    """
    Strategia
    """
    def __init__(self,algo=None):
        if algo:
            # konwersja funkcji na metodę
            # dzięki temu dynamicznie przypisana procedura będzie
            # miała dostęp do atrybutów klasy (będzie do niej przesyłany
            # argument 'self'
            self.algo = types.MethodType(algo, self)

    def sort(self,iterable):
        if self.algo is not None:
            return self.algo(copy(iterable))
        else:
            raise NotImplemented

    
def shellSort(self, array):
     # // - dzielenie całkowitoliczbowe
    gap = len(array) // 2
    while gap > 0:
        for i in range(gap, len(array)):
            val = array[i]
            j = i
            while j >= gap and array[j - gap] > val:
                array[j] = array[j - gap]
                j -= gap
            array[j] = val
        gap //= 2
    return array

def heapSort(self, A):
    
    def heapify(A):
        start = (len(A) - 2) // 2
        while start >= 0:
            siftDown(A, start, len(A) - 1)
            start -= 1

    def siftDown(A, start, end):
        root = start
        while root * 2 + 1 <= end:
            child = root * 2 + 1
            if child + 1 <= end and A[child] < A[child + 1]:
                child += 1
            if child <= end and A[root] < A[child]:
                A[root], A[child] = A[child], A[root]
                root = child
            else:
                return
            
    heapify(A)
    end = len(A) - 1
    while end > 0:
        A[end], A[0] = A[0], A[end]
        siftDown(A, 0, end - 1)
        end -= 1
    return A

def quickSort(self,array):
    def qsort(array):
        if array == []: 
            return []
        else:
            pivot = array.pop(randrange(len(array)))
            lesser = qsort([l for l in array if l < pivot])
            greater = qsort([l for l in array if l >= pivot])
            return lesser + [pivot] + greater
    return qsort(array[:])

def test():
    # lista 10 losowych liczba całkowitych
    array = [randint(0,10) for _ in range(10)]
    
    sorter = Sorter(shellSort)
    print(sorter.sort(array))
    
    sorter = Sorter(quickSort)
    print(sorter.sort(array))
    
    sorter = Sorter(heapSort)
    print(sorter.sort(array))

if __name__ == "__main__":
    test()
