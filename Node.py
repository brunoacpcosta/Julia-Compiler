class Node:

    def __init__(self):
        self.value = None
        self.children = []

    def Evaluate(self):
        print("Node Evaluate")

class BinOp(Node):

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self):
        c1 = self.children[0].Evaluate()
        c2 = self.children[1].Evaluate()
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

    def Evaluate(self):
        c = self.children[0].Evaluate()
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

    def Evaluate(self):
        result = self.value
        return result


class NoOp(Node):

    def Evaluate(self):
        print("NoOp Evaluate")
