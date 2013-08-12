"""
Treść zadania:

Mamy trzy rozne rodzaje reprezentacji danych w pliku: XML, CSV oraz
FIXED length (dla ostatniego rodzaju zalozmy ze wszystkie pola maja
dlugosc 8).
Zaimplementuj program, ktory umozliwi zapisywanie danych dotyczacych
kilku wybranych rodzajow formatow dat (np YYYYMMDD, MMDDYYYY, DDMMYY -
nie bierzemy pod uwage separatorow) dla trzech powyzszych rodzajow
reprezentacji danych w pliku.
Na szczycie hierarchii klas powinny sie znajdowac
DateFormat (m.in. z metoda write()) oraz OutputFile z metodami
writeXML(), writeCSV(), writeFIDEX().
"""


import abc
import datetime
from collections import namedtuple

# struktura do przechowywania danych o dacie
DateISO = namedtuple("Date",["year","month","day"])
DateUSA = namedtuple("Date",["year","day","month"])

class DataFormat(metaclass=abc.ABCMeta):
    """
    Implementor
    """
    def __init__(self, date=None, filename=None):
        self.date = date
        self.filename = filename

    @abc.abstractmethod
    def write(self,date):
        pass

    def setDate(self, date):
        self.date = date

    def setFile(self, filename):
        self.filename = filename


class CSVData(DataFormat):
    """
    Concrete implementor
    """
    def write(self,date=None):
        if date is not None:
            self.date = date
        with open(self.filename,"w+") as file:
            d = ",".join(map(str,self.date))
            print(d)
            file.write(d)


class XMLData(DataFormat):
    """
    Concrete implementor
    """
    def write(self,date=None):
        if date is not None:
            self.date = date
        with open(self.filename, "w+") as file:
            d = "<date>"+"-".join(map(str,self.date))+"</date>"
            print(d)
            file.write(d)


class FixedLenData(DataFormat):
    """
    Concrete implementor
    """
    def write(self,date=None):
        if date is not None:
            self.date = date
        with open(self.filename, "w+") as file:
            d = "".join(map(str,self.date)).rjust(8,"-")
            print(d)
            file.write(d)


DataFormat.register(CSVData)
DataFormat.register(XMLData)
DataFormat.register(FixedLenData)


class State(metaclass=abc.ABCMeta):
    """
    State
    """
    @abc.abstractmethod
    def toggle(self):
        pass

    @abc.abstractmethod
    def getDate(self):
        pass


class CompactState(State):
    """
    Concrete state

    Rok zapisywany za pomocą dwóch cyfr
    """   
    def toggle(self):
        return FullState()

    def getDate(self):
        d = datetime.date.today()
        return DateISO(year=str(d.year)[2:],
                       month=str(d.month).zfill(2),
                       day=str(d.day).zfill(2))


class FullState(State):
    """
    Concrete state

    Rok zapisywany za pomocą czterech cyfr
    """
    def toggle(self):
        return CompactState()
        
    def getDate(self):
        d = datetime.date.today()
        return DateISO(year=str(d.year),
                       month=str(d.month).zfill(2),
                       day=str(d.day).zfill(2))


State.register(CompactState)
State.register(FullState)


class OutputFile(object):
    """
    Abstraction

    Tworzy w konstruktorze jeden, odpowiedni obiekt implementacji

    Przechowuje dane o stanie (trybie) zapisu: krótki/pełny
    """
    def __init__(self,filename,format_="csv"):
        self.filename = filename
        self.__state = FullState()
        if format_ == "csv":
            self.__format = CSVData(filename=self.filename)
        elif format_ == "xml":
            self.__format = XMLData(filename=self.filename)
        elif format_ == "fixedLen":
            self.__format = FixedLenData(filename=self.filename)
    
    def writeUSADateFormat(self):
        d = self.__state.getDate()
        d = DateUSA(year=d.year,
                    day=d.day,
                    month=d.month)
        self.__format.write(d)

    def writeISODateFormat(self):
        d = self.__state.getDate()
        d = DateISO(year=d.year,
                    day=d.day,
                    month=d.month)
        self.__format.write(d)

    def toggleCompact(self):
        self.__state = self.__state.toggle()
        


def test():
    out = OutputFile("date.csv",format_="csv")
    out.writeUSADateFormat()
    out.writeISODateFormat()
    #zmieniamy tryb na krótki (rok zapisywany dwiema cyframi)
    out.toggleCompact()
    out.writeUSADateFormat()
    out.writeISODateFormat()
    
    out = OutputFile("date.xml",format_="xml")
    out.writeUSADateFormat()
    out.writeISODateFormat()
    out.toggleCompact()
    out.writeUSADateFormat()
    out.writeISODateFormat()

    out = OutputFile("date.txt",format_="fixedLen")
    out.writeUSADateFormat()
    out.writeISODateFormat()
    out.toggleCompact()
    out.writeUSADateFormat()
    out.writeISODateFormat()
    
if __name__ == "__main__":
    test()

