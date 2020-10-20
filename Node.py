class Node:

    def __init__(self):
        self.value = None
        self.children = []

    def Evaluate(self, symbolTable):
        print("Node Evaluate")

    def __repr__(self):
        return f"//{self.value} | {self.children}\\\\"


class BinOp(Node):

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        c1 = self.children[0].Evaluate(symbolTable)
        c2 = self.children[1].Evaluate(symbolTable)
        result = None
        if self.value == "PLUS":
            result = c1 + c2
        elif self.value == "MINUS":
            result = c1 - c2
        elif self.value == "TIMES":
            result = c1 * c2
        elif self.value == "DIVIDED":
            result = int(c1 / c2)
        elif self.value == "GREATER":
            result = c1 > c2
        elif self.value == "LESS":
            result = c1 < c2
        elif self.value == "EQUALS":
            result = (c1 == c2)
        elif self.value == "AND":
            result = bool(c1 and c2)
        elif self.value == "OR":
            result = bool(c1 or c2)
        return result


class UnOp(Node):

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        c = self.children[0].Evaluate(symbolTable)
        result = None
        if self.value == "PLUS":
            result = 1 * c

        elif self.value == "MINUS":
            result = -1 * c

        elif self.value == "NOT":
            result = bool(not c)

        return result


class IntVal(Node):

    def __init__(self, value):
        self.value = value
        self.children = []

    def Evaluate(self, symbolTable):
        result = self.value
        return result


class NoOp(Node):

    def Evaluate(self, symbolTable):
        pass


class Println(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        print(self.children[0].Evaluate(symbolTable))


class Statements(Node):
    def __init__(self):
        self.value = "BLOCK"
        self.children = []

    def Evaluate(self, symbolTable):
        for child in self.children:
            child.Evaluate(symbolTable)


class Identifier(Node):
    def __init__(self, value):
        self.value = value
        self.children = []

    def Evaluate(self, symbolTable):
        return symbolTable.getVar(self.value)


class Assignment(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        symbolTable.setVar(
            self.children[0].value, self.children[1].Evaluate(symbolTable))


class ReadLine(Node):
    def __init__(self):
        self.value = None
        self.children = []

    def Evaluate(self, symbolTable):
        readLine = int(input())
        self.value = readLine
        return self.value


class While(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        while self.children[0].Evaluate(symbolTable) == True:
            self.children[1].Evaluate(symbolTable)
        return


class If(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        if self.children[0].Evaluate(symbolTable) == True:
            self.children[1].Evaluate(symbolTable)

        else:
            if len(self.children) == 3:
                self.children[2].Evaluate(symbolTable)