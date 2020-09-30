class Node:

    def __init__(self):
        self.value = None
        self.children = []

    def Evaluate(self, symbolTable):
        print("Node Evaluate")

class BinOp(Node):

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        c1 = self.children[0].Evaluate(symbolTable)
        c2 = self.children[1].Evaluate(symbolTable)
        if self.value == "PLUS":
            result = c1 + c2
            return result
        elif self.value == "MINUS":
            result = c1 - c2
            return result
        elif self.value == "TIMES":
            result = c1 * c2
            return result
        elif self.value == "DIVIDED":
            result = int(c1 / c2)
            return result

class UnOp(Node):

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        c = self.children[0].Evaluate(symbolTable)
        if self.value == "PLUS":
            result = 1 * c
            return result
        elif self.value == "MINUS":
            result = -1 * c
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
        print("NoOp Evaluate")

class Println(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        print(self.children[0].Evaluate(symbolTable))

class Block(Node):
    def __init__(self):
        self.value = None
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
        symbolTable.setVar(self.children[0].value, self.children[1].Evaluate(symbolTable))
