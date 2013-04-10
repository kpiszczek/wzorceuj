#!/usr/bin/python
# -*- coding: utf-8 -*-

import abc
from tkinter import Tk, Frame, Label, Button

class Form(object):
    """
    Produkt
    """
    def __init__(self):
        self.message = None
        self.buttons = None

    def __str__(self):
        return 'message: "%s", buttons: %s' % (self.message,self.buttons)


class FormBuilder(object):
    """
    Kierownik
    """
    def __init__(self):
        self.but_builder = None
        self.wm_builder = None
        
    def constructForm(self):
        # tworzymy formularz tylko wtedy gdy istnieją budowniczowie
        if self.but_builder is not None and self.wm_builder is not None:
            self.but_builder.new_form()
            self.but_builder.addButtons()
            self.wm_builder.form = self.but_builder.form
            self.wm_builder.printWM()

    def setButtonsBuilder(self,but_builder):
        self.but_builder = but_builder

    def setWMBuilder(self,wm_builder):
        self.wm_builder = wm_builder

    def getForm(self):
        return self.wm_builder.form


class Builder(object):
    """
    Budowniczy
    """
    def __init__(self):
        self.form = None

    def new_form(self):
        self.form = Form()

    
class ButtonsBuilder(Builder,metaclass=abc.ABCMeta):
    """
    Budowniczy
    """
    @abc.abstractmethod
    def addButtons(self):
        pass


class StudentsButtonsBuilder(ButtonsBuilder):
    """
    Budowniczy konkretny
    """
    def addButtons(self):
        self.form.buttons = ('Aktualności','Plan zajęć', 'Oceny')


class AdminButtonsBuilder(ButtonsBuilder):
    """
    Budowniczy konkretny
    """
    def addButtons(self):
        self.form.buttons = ('Aktualności', 'Użytkownicy', 'Prowadzący')


ButtonsBuilder.register(StudentsButtonsBuilder)
ButtonsBuilder.register(AdminButtonsBuilder)


class WelcomeMessageBuilder(metaclass=abc.ABCMeta):
    """
    Budowniczy
    """
    @abc.abstractmethod
    def printWM(self):
        pass
        

class StudentsWMBuilder(WelcomeMessageBuilder):
    """
    Budowniczy konkretny
    """
    def printWM(self):
        self.form.message = "Witaj! Już po sesji?"


class AdminWMBuilder(WelcomeMessageBuilder):
    """
    Budowniczy konkretny
    """
    def printWM(self):
        self.form.message = "Hej! Na co się dzisiaj skarżą użyszkodnicy?"


WelcomeMessageBuilder.register(StudentsWMBuilder)
WelcomeMessageBuilder.register(AdminWMBuilder)


class Window(Frame):
    """
    Klasa pomocnicza do wyświetlenia formularza
    """
    def __init__(self,parent,form):
        super(Window,self).__init__(parent)
        self.parent = parent
        self.message = Label(self,text=form.message)
        self.message.pack(padx=10,pady=10)
        self.buttons = [Button(self,text=b) for b in form.buttons]
        for button in self.buttons:
            button.pack(side="left", padx=10,pady=10)            
        self.pack()


def test():
    form_builder = FormBuilder()
    but_builder = StudentsButtonsBuilder()
    wm_builder = StudentsWMBuilder()

    form_builder.setButtonsBuilder(but_builder)
    form_builder.setWMBuilder(wm_builder)

    form_builder.constructForm()
    
    form = form_builder.getForm()

    # tworzenie okna programu    
    root = Tk()
    w = Window(root,form)
    root.geometry("400x100+100+100")
    root.mainloop()

if __name__ == "__main__":
    test()
