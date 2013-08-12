"""
Treśc zadania:

Prosze zaimplementowac klase abstrakcyjna (interfejs) User (z
nastepujacymi metodami get/setName(); get/setSurname(); add(); remove()).
Nastepnie prosze stwozyc klase RealClient iplementujaca powyzszy
inferfejs. Na koniec prosze odpowiednie doimplementowac do tego klase
ProxyClient z odpowiednimi metodami.
"""


# abc - Abstract Base Classes
import abc

"""ze względu na brak interfejsów w języku Python
wykorzystuje mechanizm klas abstrakcyjnych """
class User(metaclass=abc.ABCMeta):
    def __init__(self):
        self.name = ""
        self.surname = ""
        
    def getName(self):
        return self.name
    def setName(self,name):
        self.name = name

    def getSurname(self):
        return self.surname
    def setSurname(self,surname):
        self.surname = surname

    @abc.abstractmethod
    def add(self):
        pass
    
    @abc.abstractmethod
    def remove(self):
        pass

class RealClient(User):
    def __init__(self,name, surname):
        self.name = name
        self.surname = surname
        self.atributes = dict()

    def add(self,key,value):
        self.atributes[key] = value

    def remove(self,key):
        if key in self.atributes.keys():
            del self.atributes[key]


class MaxActiveUsersReached(Exception):
    pass


"""klasa pośrednika ogranicza ilość obsługiwanych klientów oraz
możliwość dodawania/usuwania atrybutów w zależności od trybu pracy"""
class ProxyClient(User):
    user_count = 0
    max_users = 10
    def __init__(self,name, surname, mode="read",max_users=10):
        self.__mode = mode
        ProxyClient.max_users = max_users
        if ProxyClient.user_count < ProxyClient.max_users:
            ProxyClient.user_count += 1
            self.__real_client = RealClient(name,surname)
        else:
            raise MaxActiveUsersReached

    def getName(self):
        return self.__real_client.getName();

    def setName(self,name):
        return self.__real_client.setName(name);

    def getSurname(self):
        return self.__real_client.getSurname();

    def setSurname(self,surname):
        return self.__real_client.setSurname(surname);

    def add(self,key,val):
        if self.__mode == "write" or self.__mode == "append":
            self.__real_client.add(key,val)

    def remove(self,key):
        if self.__mode == "write":
            self.__real_client.remove(key)

    def __getitem__(self,key):
        try:
            return self.__real_client.atributes[key]
        except KeyError:
            return None

    def setMode(self,mode):
        self.__mode = mode

    

""" zapewnienie, że obiekty klas RealClient oraz ProxyClient
implementują wszystkie metody abstrakcyjne klasy User """
User.register(RealClient)
User.register(ProxyClient)

def test():
    users = [ProxyClient("Jan", "Testowy%s" % i) for i in range(10)]
    try:
        # nie możemy dodać więcej użytkowników
        users.append(ProxyClient("Jan","Testowy10"))
    except MaxActiveUsersReached:
        print("MaxActiveUsersReached")
    user = users[0]
    #nie możemy dodać atrybutu ponieważ pośrednik jest w trybie "read"
    user.add('phone','666-666-666') 
    print(user['phone'])
    #po zmianie trybu pracy można dodać atrybut
    user.setMode("write")
    user.add('phone','666-666-666')
    print(user['phone'])

if __name__ == "__main__":
    test()


   
