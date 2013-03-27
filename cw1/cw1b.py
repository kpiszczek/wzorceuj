#!/usr/bin/python
# -*- coding: utf-8 -*-

#Fasada
def singleton(cls):
    instances = dict()
    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance

@singleton
class ManagmentSystem:
    def __init__(self):
        self.clients = set()
        self.instruments = set()
    def addClient(self,client):
        self.clients.add(client)
    def removeClient(self,client):
        if client in self.clients:
            self.clients.remove(client)           
    def clientsInstruments(self,client):
        return client.instruments

class Client:
    #atrybut klasy
    counter = 0
    def __init__(self,name):
        self.instruments = []
        self.id = Client.counter
        Client.counter += 1
        self.name = name
    def buyInstrument(self,instr):
        self.instruments.append(instr)            
    def sellInstrument(self,insrt):
        if instr in instruments:
            self.intruments.remove(instr)

class Instrument:
    def __init__(self,manager,name):
        self.manager = manager
        self.name = name
    def register(self):
        self.manager.instruments.add(self)
    def unregister(self):
        self.manager.instruments.remove(self)
        
class API:
    manager = ManagmentSystem()
    def __init__(self):
        pass
    # metoda prywatna
    def __getClient(self,name):
        for client in API.manager.clients:
            if client.name == name:
                return client
    # metoda prywatna
    def __getInstrument(self,name):
        for instr in API.manager.instruments:
            if instr.name == name:
                return instr
            
    def existsClient(self,name):
        return any(c.name == name for c in API.manager.clients)
    
    def existsInstrument(self,name):
        return any(i.name == name for i in API.manager.instruments)
            
    def addInstrument(self,name):
        instr = Instrument(API.manager,name)
        instr.register()
        
    def removeInstrument(self,name):
        self.__getInstrument(name).unregister()
                
    def addNewClient(self,name):
        API.manager.addClient(Client(name))
        
    def removeClient(self,name):
        API.manager.removeClient(self.__getClient(name))

    def buyInstrument(self,clientName,instrName):
        self.__getClient(clientName).buyInstrument(self.__getInstrument(instrName))

    def sellInstrument(self,clientName,instrName):
        self.__getClient(clientName).sellInstrument(self.__getInstrument(instrName))

    def clientsInstruments(self,clientName):
        return API.manager.clientsInstruments(self.__getClient(clientName))

def test():
    api = API()
    api.addNewClient("Jan Testowy")
    print("istnieje klient:", api.existsClient("Jan Testowy"))
    api.removeClient("Jan Testowy")
    print("istnieje klient:", api.existsClient("Jan Testowy"))

    api.addNewClient("Jan Testowy")
    api.addInstrument("Tytuł uczestnictwa")
    print("instnieje instrument:",api.existsInstrument("Tytuł uczestnictwa"))
    api.buyInstrument("Jan Testowy","Tytuł uczestnictwa")
    print("instrumenty klienta:")
    for i in api.clientsInstruments("Jan Testowy"): print("-", i.name)

if __name__ == "__main__":
    test()

    
