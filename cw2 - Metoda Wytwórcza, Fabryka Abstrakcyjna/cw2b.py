"""
Treść zadania:

Mamy plik konfiguracyjny zawierajacy dwie informacje: w jakim kraju
sie znajdujemy i czy jestesmy w nizszym, czy wyzszym progu podatkowym
i skladkowym.
Dane na temat poziomow opodatkowania i skladek (nie majace nic
wspolnego z rzeczywistoscia):
Podatek
Polska (nizszy prog 18, wyzszy 32)
USA    (nizszy 10, wyzszy 20)
Niemcy (nizszy 15, wyzszy 25)
Skladka
Polska (nizszy 28, wyzszy 42)
USA    (nizszy 20, wyzszy 40)
Niemcy (nizszy 25, wyzszy 45)

Prosze zaprojektowac abstrakcyjne klasy Tax i SupplementaryPayment z
metoda calculate(...) wypisujaca podstawe naliczenia, procent i
obliczona kwote (podatku lub skladki)
  a takze odpowiednie klasy pochodne.

Prosze rowniez zaprojektowac klase Factory i jej klasy pochodne.
Factory musi zczytywac konfiguracje z pliku.

Projekt powinien byc skonstruowany tak, zeby zadzialal z nastepujaca
funkcja main (to przyklad dla Java - moze zawierac literowki).

public class Application {

    public static void main(String[] args) {
        Double baseAmount = 100000;

        Factory fact = Factory.get();
        SupplementaryPayment sp = fact.createSP();
        Double amountToTax = sp.calculate(baseAmount);

        Tax tax = fact.createTax();
        tax.calculate(amountToTax);
    }
}
"""


import abc


"""
Klasy podatków oraz składek
"""
class Tax(metaclass=abc.ABCMeta):
    """
    Klasa abstrakcyjna
    """
    def __init__(self,thresh="low"):
        self.thresh = thresh
        self.low = 0
        self.high = 0
    @abc.abstractmethod
    def calculate(self,amount):
        if self.thresh == "low":
            percent = self.low
        elif self.thresh == "high":
            percent = self.high
        else:
            raise ValueError("zła wartość progu")
        print("Base amount:", "%0.2f" % amount)
        print("Tax:", percent, "%")
        print("Tax amount:", "%0.2f" % (amount*percent/100))
        return amount*(1 - percent/100)

class SupplementaryPayment(metaclass=abc.ABCMeta):
    """
    Klasa abstrakcyjna
    """
    def __init__(self,thresh="low"):
        self.thresh = thresh
        self.low = 0
        self.high = 0
    @abc.abstractmethod
    def calculate(self,amount):
        if self.thresh == "low":
            percent = self.low
        elif self.thresh == "high":
            percent = self.high
        else:
            raise ValueError("zła wartość progu")
        print("Base amount:", "%0.2f" % amount)
        print("Supplementary payment:", percent, "%")
        print("Supplementary amount:", "%0.2f" % (amount*percent/100))
        return amount*(1 - percent/100)

class PolandTax(Tax):
    """
    Klasa konkretna
    """
    def __init__(self,*args,**kwargs):
        super(PolandTax,self).__init__(*args,**kwargs)
        self.low = 18
        self.high = 32
    def calculate(self,amount):
        return super(PolandTax,self).calculate(amount)

class USATax(Tax):
    """
    Klasa konkretna
    """
    def __init__(self,*args,**kwargs):
        super(USATax,self).__init__(*args,**kwargs)
        self.low = 10
        self.high = 20        
    def calculate(self,amount):
        return super(USATax,self).calculate(amount)

class GermanyTax(Tax):
    """
    Klasa konkretna
    """
    def __init__(self,*args,**kwargs):
        super(GermanyTax,self).__init__(*args,**kwargs)
        self.low = 15
        self.high = 25       
    def calculate(self,amount):
        return super(GermanyTax,self).calculate(amount)

class PolandSupplementaryPayment(SupplementaryPayment):
    """
    Klasa konkretna
    """
    def __init__(self,*args,**kwargs):
        super(PolandSupplementaryPayment,self).__init__(*args,**kwargs)
        self.low = 28
        self.high = 42
    def calculate(self,amount):
        return super(PolandSupplementaryPayment,self).calculate(amount)
    
class USASupplementaryPayment(SupplementaryPayment):
    """
    Klasa konkretna
    """
    def __init__(self,*args,**kwargs):
        super(USASupplementaryPayment,self).__init__(*args,**kwargs)
        self.low = 20
        self.high = 40
    def calculate(self,amount):
        return super(USASupplementaryPayment,self).calculate(amount)
    
class GermanySupplementaryPayment(SupplementaryPayment):
    """
    Klasa konkretna
    """
    def __init__(self,*args,**kwargs):
        super(GermanySupplementaryPayment,self).__init__(*args,**kwargs)
        self.low = 25
        self.high = 45
    def calculate(self,amount):
        return super(GermanySupplementaryPayment,self).calculate(amount)

"""
Zapewnienie, że wszsystkie obiekty klas konkretnych implemnetują
metody abstrakcyjne odpowiednich klas bazowych
"""
Tax.register(PolandTax)
Tax.register(USATax)
Tax.register(GermanyTax)
SupplementaryPayment.register(PolandSupplementaryPayment)
SupplementaryPayment.register(USASupplementaryPayment)
SupplementaryPayment.register(GermanySupplementaryPayment)


"""
Klasy fabryczne
"""
class Factory(metaclass=abc.ABCMeta):
    """
    Klasa abstrakcyjna
    """
    country = None
    supp_thresh = None
    tax_thresh = None
    @staticmethod
    def get():
        current_country = None
        values = set(("low","high"))
        with open(".conf",'r') as f:
            country, supp_thresh, tax_thresh = f.readline().split()
            Factory.country = country
            if supp_thresh in values and tax_thresh in values:
                Factory.tax_thresh = tax_thresh
                Factory.supp_thresh = supp_thresh
            else:
                raise ValueError("Błędny plik konfiguracyjny")
        if Factory.country == "Poland":
            return PolandFactory()
        elif Factory.country == "USA":
            return USAFactory()
        elif Factory.country == "Germany":
            return GermanyFactory()
    
    @abc.abstractmethod
    def createSP(self):
        pass
    @abc.abstractmethod
    def createTax(self):
        pass

class PolandFactory(Factory):
    """
    Klasa konkretna
    """
    def createTax(self):
        return PolandTax(self.tax_thresh)
    def createSP(self):
        return PolandSupplementaryPayment(self.supp_thresh)

class GermanyFactory(Factory):
    """
    Klasa konkretna
    """
    def createTax(self):
        return GermanyTax(self.tax_thresh)
    def createSP(self):
        return GermanySupplementaryPayment(self.supp_thresh)

class USAFactory(Factory):
    """
    Klasa konkretna
    """
    def createTax(self):
        return USATax(self.tax_thresh)
    def createSP(self):
        return USASupplementaryPayment(self.supp_thresh)

"""
Zapewnienie, że wszsystkie obiekty klas konkretnych implemnetują
metody abstrakcyjne klasy Factory
"""    
Factory.register(PolandFactory)
Factory.register(GermanyFactory)
Factory.register(USAFactory)

def test():
    baseAmount = 100000

    fact = Factory.get()
    sp = fact.createSP()
    amountToTax = sp.calculate(baseAmount)
    
    tax = fact.createTax()
    tax.calculate(amountToTax)


if __name__ == "__main__":
    test()
            
            
