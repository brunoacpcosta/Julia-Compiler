class SymbolTable:
    def __init__(self):
        self.table = {}
        self.ebp = 1

    def getVar(self, name):
        if name not in self.table:
            raise Exception("Variable {} not declared.".format(name))
        return self.table[name]

    def setVar(self, name, value):
        if name not in self.table:
            raise Exception("Variable {} not declared.".format(name))

        variable = self.getVar(name)
        if (variable[1] == value[1]):
            self.table[name][0] = value[0]
            # print(variable[0], value[0])
        else:
            raise Exception("Invalid variable type: old {} with new {}".format(variable[1], value[1]))

    def declareVar(self, name, type):
        if (name in self.table):
            raise Exception("{}, already declared".format(name))
        # print(self.table)
        self.table[name] = [None, type, self.ebp]
        self.ebp += 1