"""
Treść zadania:

Prosze zaprojektowac nastepujaca hierarchie klas:
Abstrakcyjna klasa bazowa Shape.  Klasy pochodne: Square, Rectangle,
Triange z konstruktorami i metoda draw().
Metoda draw() nie musi ladnie rysowac danej figury geometrycznej, ale
jakos ja powinna prezentowac na ekranie.
Nastepnie do kazdej klasy prosze napisac klasy ShapeCreator,
RectangleCreator etc z metodami factory(), implementujace wzorzec
Factory Method.

W funkcji main utworz po kilka obiektow klas Rectangle i Triangle a
nastepnie wywolaj draw() dla kazdego z obiektow.
"""


import abc
import math

"""
Klasy kształtów 
"""
class Shape(metaclass=abc.ABCMeta):
    def __init__(self,outline="#000"):
        self.outline = outline
    """
    Klasa abstrakcyjna
    """
    @abc.abstractmethod
    def draw(self,canvas,x=0,y=0):
        pass
    
class Rectangle(Shape):
    """
    Klasa konkretna
    """
    def __init__(self,a=1,b=1,*args,**kwargs):
        super(Rectangle,self).__init__(*args,**kwargs)
        self.a = a
        self.b = b
        
    def draw(self,canvas,x=0,y=0):
        canvas.create_rectangle(x, y, x + self.a, y + self.b, 
            outline=self.outline, fill="#fff")

class Square(Shape):
    """
    Klasa konkretna 
    """
    def __init__(self,a=1,*args,**kwargs):
        super(Square,self).__init__(*args,**kwargs)
        self.a = a
        
    def draw(self,canvas,x=0,y=0):
        canvas.create_rectangle(x, y, x + self.a, y + self.a, 
            outline=self.outline, fill="#fff")
    
class Triangle(Shape):
    """
    Klasa konkretna
    """
    def __init__(self,a=1,b=1,c=1,*args,**kwargs):
        super(Triangle,self).__init__(*args,**kwargs)
        t = sorted((a,b,c),reverse=True)
        if t[0] > t[1] + t[2]: raise ValueError
        self.a = a
        self.b = b
        self.c = c
        
    def draw(self,canvas,x=0,y=0):
        def angle (a, b, c):
            return math.acos((c**2 - b**2 - a**2)/(-2.0 * a * b))
        ang = angle(self.a,self.b,self.c)
        canvas.create_polygon(x,
                              y,
                              x+self.a,
                              y,
                              x+self.a-self.b*math.cos(ang),
                              y+self.b*math.cos(ang),
                              outline=self.outline,
                              fill="#fff")
                              
"""
Zapewnienie, że klasy konkretne implementują wszystkie metody
abstrakcyjne klasy Shape
"""
Shape.register(Rectangle)
Shape.register(Square)
Shape.register(Triangle)
"""
=========================================================================
"""
"""
Klasy fabryczne
"""
class ShapeCreator(metaclass=abc.ABCMeta):
    """
    klasa abstrakcyjna
    """
    @abc.abstractmethod
    def factory(self,*args,**kwargs):
        return None

class RectangleCreator(ShapeCreator):
    """
    klasa konkretna
    """
    def factory(self,name,*args,**kwargs):
        if name.lower() == "rectangle":
            return Rectangle(*args,**kwargs)
        else:
            return super(RectangleCreator,self).factory(*args,**kwargs)
    
class SquareCreator(ShapeCreator):
    """
    klasa konkretna
    """
    def factory(self,name,*args,**kwargs):
        if name.lower() == "square":
            return Square(*args,**kwargs)
        else:
            return super(SquareCreator,self).factory(*args,**kwargs)
        
class TriangleCreator(ShapeCreator):
    """
    klasa konkretna
    """
    def factory(self,name,*args,**kwargs):
        if name.lower() == "triangle":
            return Triangle(*args,**kwargs)
        else:
            return super(TriangleCreator,self).factory(*args,**kwargs)

"""
Zapewnienie, że klasy konkretne implementują wszystkie metody
abstrakcyjne klasy ShapeCreator
"""       
ShapeCreator.register(RectangleCreator)
ShapeCreator.register(SquareCreator)
ShapeCreator.register(TriangleCreator)
"""
========================================================================
"""

"""
metoda 2 - w zadanym przypadku, gdy mamy do czynienia z odwzorowaniem
jeden do jednego (jedna klasa konkretna - jedna klasa fabryczna)
możemy wykorzystać do dynamicznego tworzenia obiektów funkcję wbudowana
globals() zwaracającą przestrzeń nazw modułu w postaci słownika.
"""
def shapeFactory(name,*args,**kwargs):
    if name in globals().keys():
        return globals()[name](*args,**kwargs)
    
from tkinter import Tk, Canvas, Frame, BOTH

class Window(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.canvas = Canvas(self)
        self.parent.title("Shapes")
        self.pack(fill=BOTH, expand=1)

    def drawShape(self,shape,x,y):
        shape.draw(canvas=self.canvas,x=x,y=y)
        self.canvas.pack(fill=BOTH, expand=1)
        
def test():
    """
    Kolorem czarnym są narysowane obiekty utworzone
    za pomocą klas fabrycznych.
    Kolorem czerwonym obiekty utworzone przy użyciu
    funkcji shapeFactory
    """
    creator = RectangleCreator()
    rect = creator.factory("Rectangle",a=40,b=60)
    rect2 = shapeFactory("Rectangle",a=40,b=60, outline="#f00")
    creator = TriangleCreator()
    tri = creator.factory("Triangle",a=100,b=100,c=100)
    tri2 = shapeFactory("Triangle",a=100,b=100,c=100,outline="#f00")
    creator = SquareCreator()
    sq = creator.factory("Square",a=60)
    sq2 = shapeFactory("Square",a=60,outline="#f00")
    root = Tk()
    w = Window(root)
    w.drawShape(rect,100,100)
    w.drawShape(rect2,100,200)
    w.drawShape(tri,200,100)
    w.drawShape(tri2,200,200)
    w.drawShape(sq,370,100)
    w.drawShape(sq2,370,200)
    root.geometry("600x400+100+100")
    root.mainloop()
    
if __name__ == "__main__":
    test()

