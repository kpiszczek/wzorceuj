class Observer:
    """
    Observer
    """
    def update(self, observable, arg=None):
        pass
    

class ClickObserver(Observer):
    """
    Concrete observer
    """
    def __init__(self):
        self._subject_state = "up"

    def update(self, observable, arg=None):
        if observable.getState() == "down":
            self._subject_state = observable.getState()
            print("Zdarzenie 'click' na obiekcie klasy %s" %
                  observable.__class__.__name__)


class CloseObserver(Observer):
    """
    Concrete observer
    """
    def __init__(self):
        self._subject_state = "active"

    def update(self, observable, arg=None):
        if observable.getState() == "closed":
            self._subject_state = observable.getState()
            print("Zdarzenie 'close' na obiekcie klasy %s" %
                  observable.__class__.__name__)


class SelectObserver(Observer):
    """
    Concrete observer
    """
    def __init__(self):
        self._subject_state = "idle"

    def update(self, observable, arg=None):
        if observable.getState() == "selected":
            self._subject_state = observable.getState()
            print("Zdarzenie 'select' na obiekcie klasy %s" %
                  observable.__class__.__name__)


class Observable:
    """
    Subject
    """
    def __init__(self):
        self._observers = []
        self._changed = False
        self._state = None

    def addObserver(self, observer):
        """
        Attach
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def deleteObserver(self, observer):
        """
        Detach
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def notifyObservers(self, arg=None):
        """
        Notify
        """
        if not self._changed: return
        self.clearChanged()

        for observer in self._observers:
            observer.update(self, arg)

    def setChanged(self):
        self._changed = True

    def clearChanged(self):
        self._changed = False

    def hasChanged(self):
        return self._changed



class Widget(Observable):
    """
    Subject
    """
    def __init__(self, parent=None):
        super(Widget, self).__init__()
        self._parent = parent
        self._state = None
        self._possible_states = set()

    
    def getState(self):
        return self._state

    def setState(self, state):
        # jeśli nie jest możliwa zmiana na dany stan
        # to jest on przekazywany do rodzica
        if state in self._possible_states:
            if state != self._state:
                self._state = state
                self.setChanged()
                self.notifyObservers()
        elif self._parent is not None:
            self._parent.setState(state)
        else:
            print("Akcja domyślna")

class Button(Widget):
    """
    Concrete subject
    """
    def __init__(self, parent=None):
        super(Button, self).__init__(parent)
        self._state = "up"
        self._possible_states = set(("up", "down"))


class MainWindow(Widget):
    """
    Concrete subject
    """
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self._state = "active"
        self._possible_states = set(("active", "closed"))

class Label(Widget):
    """
    Concrete subject
    """
    def __init__(self, parent=None):
        super(Label, self).__init__(parent)
        self._state = "idle"
        self._possible_states = set(("idle", "selected"))


def test():
    main = MainWindow()
    btn = Button(main)
    lbl = Label(main)
    
    clickObs = ClickObserver()
    closeObs = CloseObserver()
    selectObs = SelectObserver()
    
    btn.addObserver(clickObs)
    main.addObserver(closeObs)
    lbl.addObserver(selectObs)

    btn.setState("down")
    # propagacja zdarzenia do rodzica
    btn.setState("closed")
    lbl.setState("selected")

    # propagacja do akcji domyślnej
    lbl.setState("down")

if __name__ == "__main__":
    test()
