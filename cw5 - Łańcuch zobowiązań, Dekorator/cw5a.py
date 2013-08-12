"""
Treść zadania:

Mamy pewnien zbior klas GUI, ktore musza miec zdefiniowany
sposob na propagacje
zdarzenia typu "mouse_click" od tego obiektu, w ktorym zdarzenie mialo
miejsce a nastepnie do obiektow, ktore rzeczywiscie beda zdarzenie
obslugiwaly.
Moze tez sie zdarzyc, ze dany obiekt obsluguje wydarzenie i przekazuje
je wyzej do dalszej 'obrobki'. Zaprojektuj przykladowy zbior takich
klas i pokaz jak moga obslugiwac zdarzenia "lancuchowo".
"""


class Event:
    """
    Zdarzenie
    """
    def __init__(self, name):
        self.name = name


class Widget:
    """
    Handler
    """
    def __init__(self, parent=None):
        self._parent = parent

    def handle(self, event):
        handler = "handle_" + event.name
        # jeśli obiekt posiada metodę obsługującą dane zdarzenie
        # to zostanie on wywołana
        if hasattr(self, handler):
            method = getattr(self, handler)
            method(event)
        # jeśli nie, to zdarzenie zostanie
        # przekazane do rodzica
        elif self._parent:
            self._parent.handle(event)
        # jeśli obiekt nie posiada rodzica, a posiada
        # domyślną metodę obsługi zdarzeń to zostanie ona wywołana
        elif hasattr(self, "handle_default"):
            self.handle_default(event)
        else:
            pass


class MainWindow(Widget):
    """
    Concrete handler
    """
    def handle_close(self, event):
        print("MainWindow: " + event.name)

    def handle_default(self, event):
        print("MainWindow/default: " + event.name)


class Button(Widget):
    """
    Concrete handler
    """
    def handle_click(self, event):
        print("Button: " + event.name)
        # przekazanie zdarzenia do daleszej obróbki
        self._parent.handle(event)


class Label(Widget):
    """
    Concrete handler
    """
    def handle_select(self, event):
        print("Label: " + event.name) 


def test():
    mw = MainWindow()
    btn = Button(mw)
    lbl = Label(mw)
    btn_lbl = Label(btn)

    click = Event("click")
    close = Event("close")
    select = Event("select")

    print("\nZdarzenia 'click', 'close' i 'select' ma obiekcie klasy Label: ")
    btn_lbl.handle(click)
    btn_lbl.handle(close)
    btn_lbl.handle(select)

    print("\nZdarzenia 'click' i 'close' na obiekcie klasy Button: ")
    btn.handle(click)
    btn.handle(close)

    print("\nZdarzenie 'click' na obiekcie Label: ")
    lbl.handle(click)
    

if __name__ =="__main__":
    test()
