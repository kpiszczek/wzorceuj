import abc

class FormBuilder:
    def constructForm(self):
        pass

class ButtonsBuilder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def addButtons(self):
        pass

class StudentsButtonsBuilder(ButtonsBuilder):
    def addButtons(self):
        pass

class AdminButtonsBuilder(ButtonsBuilder):
    def addButtons(self):
        pass

ButtonsBuilder.register(StudentsButtonsBuilder)
ButtonsBuilder.register(AdminButtonsBuilder)

class WelcomeMessageBuilder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def printWM(self):
        pass

class StudentsWMBuilder(WelcomeMessageBuilder):
    def printWM(self):
        pass

class AdminWMBuilder(WelcomeMessageBuilder):
    def printWM(self):
        pass

WelcomeMessageBuilder.register(StudentsWMBuilder)
WelcomeMessageBuilder.register(AdminWMBuilder)

def test():
    pass


if __name__ == "__main__":
    test()
