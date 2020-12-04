class SymbolTable:

    def __init__(self):
        self.table = {"return" : None}

    tableFunc = {}

    def getVar(self, name):
        if name not in self.table:
            raise Exception("Variable {} not declared.".format(name))
        return self.table[name]

    def setVar(self, name, value):
        if name not in self.table:
            raise Exception("Variable {} not declared.".format(name))

        variable = self.getVar(name)
        # print(variable)
        # print(value)
        if name == "return":
            self.table[name] = value
        elif (variable[1] == value[1]):
            self.table[name][0] = value[0]
        else:
            raise Exception("Invalid variable type: old {} with new {}".format(variable[1], value[1]))

    def declareVar(self, name, type):
        if (name in self.table or name in SymbolTable.tableFunc):
            raise Exception("{}, already declared".format(name))
        # print(self.table)
        self.table[name] = [None, type]

    @staticmethod
    def getFunc(name):
        if name not in SymbolTable.tableFunc:
            raise Exception("Function {} not declared.".format(name))
        return SymbolTable.tableFunc[name]

    def declareFunc(self, name, type, reference):
        if (name in SymbolTable.tableFunc or name in self.table):
            raise Exception("{} function/var, already declared".format(name))
        SymbolTable.tableFunc[name] = [reference, type]
