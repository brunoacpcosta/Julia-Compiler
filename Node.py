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
        # print(c1, c2, self.value)
        result = None
        if (c1[1] == "String" or c2[1] == "String") and not(self.value == "TIMES" or self.value == "EQUALS"):
            raise Exception("Invalid String Operation")

        if self.value == "PLUS" or self.value == "MINUS" or self.value == "TIMES" or self.value == "DIVIDED":
            if c1[1] == "Bool":
                c1 = (int(c1[0]), c1[1])
            if c2[1] == "Bool":
                c2 = (int(c2[0]), c2[1])

            if self.value == "PLUS":
                result = (c1[0] + c2[0], "Int")
            elif self.value == "MINUS":
                result = (c1[0] - c2[0], "Int")
            elif self.value == "TIMES":
                if c1[1] == "String" or c2[1] == "String":
                    result = (str(c1[0]) + str(c2[0]), "String")
                else:
                    result = (c1[0] * c2[0], "Int")
            elif self.value == "DIVIDED":
                result = (int(c1[0] / c2[0]), "Int")
        else:
            if c1[1] == "Int" and (self.value == "OR" or self.value =="AND"):
                c1 = (c1[0] != 0, c1[1])
            if c2[1] == "Int"and (self.value == "OR" or self.value =="AND"):
                c2 = (c2[0] != 0, c2[1])

            if self.value == "GREATER":
                result = (c1[0] > c2[0], "Bool")
            elif self.value == "LESS":
                result = (c1[0] < c2[0], "Bool")
            elif self.value == "EQUALS":
                if c1[1] == "String" or c2[1] == "String":
                    if c1[1] != c2[1]:
                        raise Exception("Invalid String Operation")
                result = (c1[0] == c2[0], "Bool")
            elif self.value == "AND":
                result = (bool(c1[0] and c2[0]), "Bool")
            elif self.value == "OR":
                result = (bool(c1[0] or c2[0]), "Bool")
        return result


class UnOp(Node):

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        c = self.children[0].Evaluate(symbolTable)
        result = None
        if c[1] == "String":
            raise Exception("Invalid String Operation")
        if self.value == "PLUS":
            if c[1] == "Bool":
                c = (int(c[0]), c[1])
            result = (1 * c[0], "Int")

        elif self.value == "MINUS":
            if c[1] == "Bool":
                c = (int(c[0]), c[1])
            result = (-1 * c[0], "Int")

        elif self.value == "NOT":
            if c[1] == "Int":
                c = (c[0] != 0, c[1])
            result = (bool(not c[0]), "Bool")

        return result


class IntVal(Node):

    def __init__(self, value):
        self.value = value
        self.children = []

    def Evaluate(self, symbolTable):
        result = self.value
        return (result, "Int")


class BoolVal(Node):
    def __init__(self, value):
        self.value = value
        self.children = []

    def Evaluate(self, symbolTable):
        return (self.value, "Bool")


class StringVal(Node):
    def __init__(self, value):
        self.value = value
        self.children = []

    def Evaluate(self, symbolTable):
        return (self.value, "String")


class NoOp(Node):

    def Evaluate(self, symbolTable):
        pass


class Println(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        print(self.children[0].Evaluate(symbolTable)[0])


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
        var = symbolTable.getVar(self.value)
        return (var[0], var[1])


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
        return (self.value, "Int")


class While(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        while self.children[0].Evaluate(symbolTable)[0] == True:
            self.children[1].Evaluate(symbolTable)


class If(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        if self.children[0].Evaluate(symbolTable)[0] == True:
            self.children[1].Evaluate(symbolTable)

        else:
            if len(self.children) == 3:
                self.children[2].Evaluate(symbolTable)


class DeclareVar(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        symbolTable.declareVar(self.children[0].value, self.children[1].value)


class Type(Node):
    def __init__(self, value):
        self.value = value
        self.children = None

    def Evaluate(self, symbolTable):
        return self.value