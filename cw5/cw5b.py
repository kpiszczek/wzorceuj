from tkinter import Tk, Frame, BOTH, OptionMenu, StringVar, Label


class BicycleFrame:
    """
    Component
    """
    def __init__(self, name, price, weight):
        self.name = name
        self.price = price
        self.weight = weight
        self.travel = None


class BicycleDecorator:
    """
    Decorator
    """
    def __init__(self, name, price, weight, decorated=None):
        self.decorated = decorated
        self._name = name
        self._price = price
        self._weight = weight

    @property
    def name(self):
        return self.decorated.name

    # 'property' pozwala na odwoływanie się do metody tak jak do atrybutu
    # >>>obj.price
    # jest równoznaczne z wywołaniem
    # >>>obj.price()   
    @property
    def price(self):
        return self.decorated.price + self._price

    @property
    def weight(self):
        return self.decorated.weight + self._weight

    @property
    def travel(self):
        return self.decorated.travel


class ForkDecorator(BicycleDecorator):
    """
    Concrete decorator

    definiuje atrybut skoku amortyzatora
    """
    def __init__(self,name, price, weight, travel=100, decorated=None):
        super(ForkDecorator,self).__init__(name, price, weight, decorated)
        self._travel = travel

    @property
    def travel(self):
        return self._travel


class GroupDecorator(BicycleDecorator):
    """
    Concrete decorator
    """
    pass


class WheelsetDecorator(BicycleDecorator):
    """
    Concrete decorator
    """
    pass


class ComponentsDecorator(BicycleDecorator):
    """
    Concrete decorator
    """
    pass


class ConfigurationWindow(Frame):
    """
    Klasa GUI konfiguratora roweru

    w metodzie 'createBike' jest tworzony obiekt roweru
    z wykorzystaniem dekoratorów
    """
    def __init__(self, parent, frames, forks, wheelsets, groups, components):
        """
        inicjalizacja obiektu okna - nieistotne dla idei zdania
        """
        super(ConfigurationWindow, self).__init__(parent)
        self._bike = None
        self.parent = parent
        self.frames = frames
        self.forks = forks
        self.wheelsets = wheelsets
        self.groups = groups
        self.components = components
        self.parent.title("Bicycle configurator")
        self._bike_price = StringVar(self.parent)
        self._bike_weight = StringVar(self.parent)
        self._bike_travel = StringVar(self.parent)
        self.price_label = Label(self.parent, textvariable=self._bike_price)
        self.weight_label = Label(self.parent, textvariable=self._bike_weight)
        self.travel_label = Label(self.parent, textvariable=self._bike_travel)

        self.createInterface()
        self.createBike()

        self.price_label.pack()
        self.weight_label.pack()
        self.travel_label.pack()
        
        self.pack(fill=BOTH, expand=1)
        
    def createInterface(self):
        """
        Tworzenie interfejsu - nieistotne dla idei zadania
        """
        self.frame_choice = StringVar(self.parent)
        self.frame_choice.set(tuple(self.frames.keys())[0])
        self.frame_choice.trace("w", self.createBike)
        self.frame_options = OptionMenu(self.parent,self.frame_choice,
                                        *self.frames.keys())
        Label(self.parent,text="Rama:").pack()
        self.frame_options.pack(fill=BOTH, expand=1)

        self.fork_choice = StringVar(self.parent)
        self.fork_choice.set(tuple(self.forks.keys())[0])
        self.fork_choice.trace("w", self.createBike)
        self.fork_options = OptionMenu(self.parent,self.fork_choice,
                                        *self.forks.keys())
        Label(self.parent,text="Widelec:").pack()
        self.fork_options.pack(fill=BOTH, expand=1)

        self.wheelset_choice = StringVar(self.parent)
        self.wheelset_choice.set(tuple(self.wheelsets.keys())[0])
        self.wheelset_choice.trace("w", self.createBike)
        self.wheelset_options = OptionMenu(self.parent,self.wheelset_choice,
                                        *self.wheelsets.keys())
        Label(self.parent,text="Koła:").pack()
        self.wheelset_options.pack(fill=BOTH, expand=1)

        self.group_choice = StringVar(self.parent)
        self.group_choice.set(tuple(self.groups.keys())[0])
        self.group_choice.trace("w", self.createBike)
        self.group_options = OptionMenu(self.parent,self.group_choice,
                                        *self.groups.keys())
        Label(self.parent,text="Grupa osprzętu:").pack()
        self.group_options.pack(fill=BOTH, expand=1)

        self.components_choice = StringVar(self.parent)
        self.components_choice.set(tuple(self.components.keys())[0])
        self.components_choice.trace("w", self.createBike)
        self.components_options = OptionMenu(self.parent,self.components_choice,
                                        *self.components.keys())
        Label(self.parent,text="Komponenty:").pack()
        self.components_options.pack(fill=BOTH, expand=1)

    def createBike(self, *args):
        """
        Metoda tworząca obiekt roweru na zasadanie dekorowania
        obiektu klasy 'Frame'
        """
        frame = self.frames[self.frame_choice.get()]
        
        fork = self.forks[self.fork_choice.get()]
        fork.decorated = frame
        
        wheelset = self.wheelsets[self.wheelset_choice.get()]
        wheelset.decorated = fork
        
        group = self.groups[self.group_choice.get()]
        group.decorated = wheelset
        
        components = self.components[self.components_choice.get()]
        components.decorated = group
        self._bike = components

        # przypisanie wartości odpowiednim elementom GUI       
        self._bike_price.set("cena: " + str(self._bike.price) + "zł")
        self._bike_weight.set("waga: " + str(self._bike.weight) + " gr")
        self._bike_travel.set("skok: " + str(self._bike.travel) + " mm")

        # uaktualnienie okna
        self.price_label.update_idletasks()
        self.weight_label.update_idletasks()
        # zmiana tytułu okna
        self.parent.wm_title(self._bike.name)
        
    
def test():
    frames = {"S-works stumpjumer carbon 29":
              BicycleFrame("S-works stumpjumer carbon 29", 10000, 1180),
              "Grand Canyon CF SLX 29":
              BicycleFrame("Grand Canyon CF SLX 29", 7269, 1080),
              "Simplon Razorblade 29":
              BicycleFrame("Simplon Razorblade 29", 5800, 1190)}
    forks = {"Rock Shox SID 29 RLT":
             ForkDecorator("Rock Shox SID 29 RLT", 1800, 1620),
             "DT Swiss XMM 100 SS":
             ForkDecorator("DT Swiss XMM 100 SS", 2650, 1748)}
    wheelsets = {"Mavic Crossmax 29 SLR":
                 WheelsetDecorator("Mavic Crossmax 29 SLR", 3500, 1610),
                 "DT Swiss XM 1550 Tricon 29":
                 WheelsetDecorator("DT Swiss XM 1550 Tricon 29", 4100, 1800)}
    groups = {"Shimano XTR":
              GroupDecorator("Shimano XTR", 4299, 1950),
              "Sram X.0":
              GroupDecorator("Sram X.0", 3750, 2000)}
    components = {"Race Face NEXT":
                  ComponentsDecorator("Race Face NEXT", 1500, 540)}
    
    root = Tk()
    frame = ConfigurationWindow(root, frames, forks, wheelsets, groups, components)
    root.geometry("300x350+400+150")
    root.mainloop()

if __name__ == "__main__":
    test()
