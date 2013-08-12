#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Treść zadania:

Utworz abstrakcyjna klase Multimedia z deklaracja matody
clone() oraz toString(); jezeli chodzi o pola to powinna zawierac
przynajmniej nazwe (np domyslna) jak i typ obiektu. Prosze dodac
przynajmniej jedno pole wskaznikowe (C++) lub jego odpowiednik tak,
zeby konieczne bylo stworzenie deep copy obiektu przy klonowaniu.
Nastepnie utworz klasy do niej pochodne Picture, Music, Movie.
Klasy powinny zadzialac z ponizszym kodem.

int main(){
        std::vector<Multimedia*> my_multimedia;
        my_multimedia.push_back(new Picture);
        my_multimedia.push_back(new Music);
        my_multimedia.push_back(new Movie);

        std::vector<Multimedia*> multimedia_copy;

      for(std::vector<Multimedia*>::iterator it =
my_multimedia.begin();
          it != my_multimedia.end();
          ++it)
      {
                multimedia_copy.push_back( (*it)->clone() );
      }
      for(std::vector<Multimedia*>::iterator it2 =
my_multimedia.begin();
          it2 != my_multimedia.end();
          ++it2)
      {
                (*it2)->toString();
      }
      return 0;
}
"""


import abc
import copy
from random import random


class Multimedia(metaclass=abc.ABCMeta):
    """
    Prototyp
    """
    def __init__(self,name,type_,data=None):
        self.name = name
        self.type_ = type_
        # jeśli nie zostały przesłane dane początkowe to
        # wypełniamy obiekt losowymi danymi
        if data is None:
            self.populate_data()
        else:
            self.data = data
    
    @abc.abstractmethod
    def clone(self):
        return copy.deepcopy(self)

    @abc.abstractmethod
    def toString(self):
        return "%s: %s" % (self.type_,self.name)

    @abc.abstractmethod
    def populate_data(self):
        pass

    def __eq__(self,other):
        """
        Definicja zachowania dla operatora ==
        Pozwala na sprawdzenie czy zawartość danych
        w dwóch obiektach jest identyczna
        """
        return (self.name == other.name) and \
               (self.type_ == other.type_) and \
               (self.data == other.data)


class Picture(Multimedia):
    """
    Prototyp konkretny
    """
    def __init__(self,name="new_picture",data=None):
        # wywołanie konstruktora klasy bazowej
        super(Picture,self).__init__(name,"Picture",data)

    def clone(self):
        # wywołanie metody klasy bazowej
        return super(Picture,self).clone()

    def toString(self):
        # wywołanie metody klasy bazowej
        return super(Picture,self).toString()

    def populate_data(self):
        # tworzymy dwuwymiarową tablicę losowych
        # trójelementowych krotek (RGB) o rozmiarze 5x5
        self.data = [[(random(),random(),random())
                      for _ in range(5)]
                     for _ in range(5)]


class Music(Multimedia):
    """
    Prototyp konkretny
    """
    def __init__(self,name="new_music",data=None):
        # wywołanie konstruktora klasy bazowej
        super(Music,self).__init__(name,"Music",data)

    def clone(self):
        # wywołanie metody klasy bazowej
        return super(Music,self).clone()

    def toString(self):
        # wywołanie metody klasy bazowej
        return super(Music,self).toString()

    def populate_data(self):
        # tworzymy 256-elementową tablicę losowych wartości (próbek)
        self.data = [random() for _ in range(256)]       
        

class Movie(Multimedia):
    """
    Prototyp konkretny
    """ 
    def __init__(self,name="new_movie",data=None):
        # wywołanie konstruktora klasy bazowej
        super(Movie,self).__init__(name,"Movie",data)

    def clone(self):
        # wywołanie metody klasy bazowej
        return super(Movie,self).clone()

    def toString(self):
        # wywołanie metody klasy bazowej
        return super(Movie,self).toString()

    def populate_data(self):
        # tworzymy tablicę 25 obiektów klasy Picture
        self.data = [Picture(str(i)) for i in range(25)]
    

# zapewnienie, że wszytkie obiekty klas Picture, Music oraz Movie
# implementują wszystkie metody abstrakcyjne klasy Multimedia
Multimedia.register(Picture)
Multimedia.register(Music)
Multimedia.register(Movie)


def test():
    # tworzymy listę zawierającą po jednym obiekcie każdej klasy konkretnej
    my_multimedia = [Picture(),Music(),Movie()]

    # tworzymy listę 'klonów' elementów listy my_multimedia
    multimedia_copy = [mm.clone() for mm in my_multimedia]

    # iterujemny równolegle po elementach obu list
    # mc - element listy 'klonów', mm - element listy 'oryginałów'
    for mc, mm in zip(multimedia_copy, my_multimedia):
        print("Obiekt z listy 'my_multimedia':\t\t",mm.toString())
        print("Obiekt z listy 'multimedia_copy':\t",mc.toString())
        print("Zawartość danych jest identyczna:\t", mm.data == mc.data)
        print("Kolekcja danych to ten sam obiekt:\t", mm.data is mc.data,"\n")

if __name__ == "__main__":
    test()
