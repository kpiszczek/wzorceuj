"""abc - Abstract Base Classes """
import abc

class LegacyCar:
    def __init__(self):
        self.x = 0
        self.y = 0
    def drive(self,x,y):
        self.x += x
        self.y += y

class Racetrack:
    def __init__(self):
        self.vehicles = []
    def addVehicle(self,vehicle):
        self.vehicles.append(vehicle)

class Vehicle(metaclass=abc.ABCMeta):
    @abc.abstractmethod    
    def moveTo(self,x,y):
        return

class Adapter(Vehicle,LegacyCar):
    def moveTo(self,x,y):
        self.drive(x,y)

"""Upewniamy się, że Adapter implementuje wszystkie
metody abstakcyjne klasy Vehicle"""
Vehicle.register(Adapter)

def test():
    r = Racetrack()
    for _ in range(10): r.addVehicle(Adapter())
    #każdy pojazd utworzony za pomocą klasy Adapter jest instancją klasy Vehicle
    for v in r.vehicles: print(isinstance(v,Vehicle))
    x = 0
    y = 0
    #przesuwamy każdy z pojazdów w inne miejsce
    for v in r.vehicles:
        v.moveTo(x,y)
        x += 1
        y += 1
    for v in r.vehicles: print(v.x,v.y)

if __name__ == "__main__":
    test()
