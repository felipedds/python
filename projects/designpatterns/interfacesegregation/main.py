from abc import abstractmethod

'''
Making interfaces which feature too many elements is not a good idea,
because you're forcing your clients to define methods in this case, which
they might not even need.
'''
class Machine:
    def print(self, document):
        raise NotImplementedError
    def fax(self, document):
        raise NotImplementedError
    def scan(self, document):
        raise NotImplementedError

'''
The interface aggregation principle states that you should segregate so.
'''
class Printer:
    @abstractmethod
    def print(self, document):
        pass

class Scanner:
    @abstractmethod
    def scan(self, document):
        pass

class MyPrinter(Printer):
    @abstractmethod
    def print(self, document):
        print(document)

class Photocopier(Printer, Scanner):
    def print(self, document):
        pass

    def scan(self, document):
        pass

class MultiFunctionDevice(Printer, Scanner):
    @abstractmethod
    def print(self, document):
        pass

    @abstractmethod
    def scan(self, document):
        pass

class MultiFunctionMachine(MultiFunctionDevice):
    def __init__(self, printer, scanner):
        self.printer = printer
        self.scanner = scanner

    def print(self, document):
        pass

    def scan(self, document):
        pass

