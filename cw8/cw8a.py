import sqlite3

from datetime import datetime


class OrderManager:
    """
    Mediator
    """
    def __init__(self):
        self.__logger = None
        self.__db = None
        self.__acceptor = None
        self.__reciever = None
        self.__executor = None
        self.__order = None

    def log(self):
        self.__logger.log()
        self.__db.insert()
        print("...")
        
    def recieve(self, order):
        self.__order = order
        self.__reciever.recieve()
        self.log()

    def accept(self):
        if self.__order is not None:
            self.__acceptor.accept()
            self.log()

    def complete(self):
        if self.__order is not None:
            self.__executor.execute()
            self.log()
            self.__order = None
        
    def set_state(self, state):
        if self.__order is not None:
            self.__order.set_state(state)

    def get_state(self):
        if self.__order is not None:
            self.__order.get_state()

    def get_order_str(self):
        if self.__order is not None:
            return str(self.__order)

    def get_date(self):
        if self.__order is not None:
            return self.__order.get_date()

    def set_logger(self, logger):
        self.__logger = logger

    def set_db(self, db):
        self.__db = db

    def set_acceptor(self, acceptor):
        self.__acceptor = acceptor

    def set_reciever(self, reciever):
        self.__reciever = reciever

    def set_executor(self, executor):
        self.__executor = executor

    def set_order(self, order):
        self.__order = order


class Colleague:
    """
    Colleague
    """
    def __init__(self, mediator=None):
        self._mediator = mediator

    def set_manager(self, mediator):
        self._mediator = mediator


class Order(Colleague):
    """
    Concrete colleague
    """
    def __init__(self, user, mediator=None):
        super(Order, self).__init__(mediator)
        self.__user = user
        self.__date = str(datetime.now())
        self.__state = "Initial"

    def is_valid(self):
        if self.__state == "Completed":
            return True
        if self.__state in ("Initial", "Recievied"):
            self._mediator.accept()
        return self.__state == "Accepted"

    def complete(self):
        self._mediator.complete()        

    def set_state(self, state):
        self.__state = state

    def get_date(self):
        return self.__date

    def get_state(self):
        return self.__state

    def __str__(self):
        return "placed at: %s, placed by: %s, state: %s" % (self.__date,
                                                            self.__user,
                                                            self.__state)


class DbLogger(Colleague):
    """
    Concrete colleague
    """
    def __init__(self, mediator=None):
        super(DbLogger, self).__init__(mediator)
        self._dbname = "log.db"

    def insert(self):
        con = sqlite3.connect(self._dbname)
        cur = con.cursor()
        cur.execute("INSERT INTO Logs(Data) VALUES (?)",
                    (self._mediator.get_order_str(),))
        con.commit()
        con.close()
        print("Logged into database!")


class FileLogger(Colleague):
    """
    Concrete colleague
    """
    def __init__(self, mediator=None):
        super(FileLogger, self).__init__(mediator)
        self._filename = ".log"

    def log(self):
        f = open(self._filename, "a")
        f.write("%s, %s" % (str(datetime.now()), self._mediator.get_order_str()))
        f.close()
        print("Logged to file!")

class Reciever(Colleague):
    """
    Concrete colleague
    """
    def __init__(self, mediator=None):
        super(Reciever, self).__init__(mediator)

    def recieve(self):
        print("Performing recieving actions!")
        self._mediator.set_state("Recievied")
    
class Acceptor(Colleague):
    """
    Concrete colleague
    """
    def __init__(self, mediator=None):
        super(Acceptor, self).__init__(mediator)

    def accept(self):
        print("Performing accepting actions!")
        # akceptuje wszystkie zamówienia z 'przeszłości'
        # odrzuca zamówienia o dacie przyszłej
        if str(datetime.now()) > self._mediator.get_date():
            print("\tAccepted!")
            self._mediator.set_state("Accepted")
        else:
            print("\tRejected!")
            self._mediator.set_state("Rejected")

class Executor(Colleague):
    """
    Concrete colleague
    """
    def __init__(self, mediator=None):
        super(Executor, self).__init__(mediator)

    def execute(self):
        print("Performing execution!")
        if self._mediator.get_state() == "Accepted":
            self._mediator.set_state("Completed")
            

def test():
    manager = OrderManager()
    manager.set_logger(FileLogger(manager))
    manager.set_db(DbLogger(manager))
    manager.set_acceptor(Acceptor(manager))
    manager.set_reciever(Reciever(manager))
    manager.set_executor(Executor(manager))

    order = Order("Guest", manager)
    manager.recieve(order)

    t = order.is_valid()
    print("Order is valid: %r" % t)
    
    order.complete()
    
if __name__ == "__main__":
    test()
