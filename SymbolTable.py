class SymbolTable:
    def __init__(self):
        self.table = {}

    def getVar(self, name):
        if name not in self.table:
            raise Exception("Variable {} not declared.".format(name))
        return self.table[name]

    def setVar(self, name, value):
        self.table[name] = value