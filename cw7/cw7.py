#######################
# Klasy odwiedzających
#######################

class Visitor:
    """
    Visitor
    """
    def visit(self, node):
        raise NotImplemented


class SumVisitor(Visitor):
    """
    Visitor
    """
    def __init__(self):
        self._sum = 0

    def update(self, elem):
        self._sum += elem

    def get_sum(self):
        return self._sum


class MaxVisitor(Visitor):
    """
    Visitor
    """
    def __init__(self):
        self._max = float("-inf")

    def update(self, elem):
        self._max = elem if elem > self._max else self._max

    def get_max(self):
        return self._max


class MinVisitor(Visitor):
    """
    Visitor
    """
    def __init__(self):
        self._min = float("inf")

    def update(self, elem):
        self._min = elem if elem < self._min else self._min

    def get_min(self):
        return self._min

    
class FabCostVisitor(SumVisitor):
    """
    Concrete visitor

    Koszt produkcji części jest sumą kosztów produkcji
    podczęści (pomijamy koszt montażu)
    """
    def visit(self, part):
        self.update(part.fabricationCost())


class FabTimeVisitor(MaxVisitor):
    """
    Concrete visitor

    Czas produkcji jest najdłuższym czasem produkcji
    elementów składowych (pomijamy czas montażu)
    """
    def visit(self, part):
        self.update(part.fabricationTime())


class UsageTimeVisitor(MinVisitor):
    """
    Concrete visitor

    Średni czas użytkowania jest wartością minimalną z czasów
    użytkowania podczęści
    """
    def visit(self, part):
        self.update(part.avgUsageTime())


class YearlyCostVisitor(SumVisitor):
    """
    Concrete visitor

    Roczny koszt jest sumą kosztów podczęści
    """
    def visit(self, part):
        self.update(part.yearlyCost())


################### 
# Klasy elementów
###################


class AutoPart:
    """
    Element (node)
    """
    def __init__(self, name, fCost, fTime, uTime, yCost):
        self.name = name
        self._fabricationCost = fCost
        self._fabricationTime = fTime
        self._avgUsageTime = uTime
        self._yearlyCost = yCost
        
    def fabricationCost(self):
        return self._fabricationCost
    
    def fabricationTime(self):
        return self._fabricationTime

    def avgUsageTime(self):
        return self._avgUsageTime

    def yearlyCost(self):
        return self._yearlyCost
    

class ElectricalPart(AutoPart):
    """
    Concrete element
    """
    pass


class SuspensionPart(AutoPart):
    """
    Concrete element
    """
    pass


class BodyPart(AutoPart):
    """
    Concrete element
    """
    pass


#########################
# Klasa struktury danych
#########################


class Car:
    """
    Object structure
    """
    def __init__(self):
        self.parts = {}

    def getIterator(self, key):
        """
        Tworzy obiekt iteratora (generatora) dla zadanego elementu.
        Iterator zwaraca pojedyncze części ze zagnieżdżonej listy
        zawierającej obiekty podczęsci elementu.

        Obiekt zwaraca część po wywołaniu funkcji next(iterator).
        W momencie gdy nie pozostał już żaden element do zwrócenia
        obiekt wyrzuca wyjątek StopIteration.
        """
        def iterator(item):
            if type(item) == list:
                for sublist in item:
                    for element in iterator(sublist):
                        yield element
            else:
                yield item
        return iterator(self.parts[key])
                       

def test():
    """
    Client
    """
    c = Car()
    c.parts["computer"] = [[ElectricalPart("comp-subpart1", 10, 2, 500, 0),
                            ElectricalPart("comp-subpart2", 20, 1, 1500, 0)],
                           ElectricalPart("comp-part1", 100, 5, 2500, 10)]
    c.parts["frame"] = [BodyPart("frame-part1", 1000, 10, 10000, 0),
                        BodyPart("frame-part1", 10, 2, 10000, 0)]
    c.parts["abs"] = [SuspensionPart("abs-sus-part1", 500, 20, 1000, 50),
                      SuspensionPart("abs-sus-part2", 100, 5, 200, 150),
                      [ElectricalPart("abs-ele-part1", 2, 5, 1500, 0),
                       ElectricalPart("abs-ele-part2", 20, 2, 2500, 5)]]

    # przechodzimy po każdej części samochodu (w naszym przypadku
    # są to: computer, frame oraz abs)
    for part in c.parts.keys():
        fabCost = FabCostVisitor()
        fabTime = FabTimeVisitor()
        useTime = UsageTimeVisitor()
        yearCost = YearlyCostVisitor()
        print("Wartości dla %s:" % part)

        subpartIter = c.getIterator(part)
        try:
            while(1):
                subpart = next(subpartIter)
                fabCost.visit(subpart)
                fabTime.visit(subpart)
                useTime.visit(subpart)
                yearCost.visit(subpart)
        except StopIteration:
            pass

        print("- koszt produkcji: %d $" % fabCost.get_sum())
        print("- czas produkcji: %d dni" % fabTime.get_max())
        print("- średni czas do zużycia: %d dni" % useTime.get_min())
        print("- średni koszt eksploatacji na rok: %d $\n" % yearCost.get_sum())


if __name__ == "__main__":
    test()
