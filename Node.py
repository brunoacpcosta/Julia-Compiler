class Node:
    i = 0
    def __init__(self):
        self.value = None
        self.children = []
        self.i = Node.newId()

    def Evaluate(self, symbolTable, compiler):
        print("Node Evaluate")

    def __repr__(self):
        return f"//{self.value} | {self.children}\\\\"

    @staticmethod
    def newId():
        # print(Node.i)
        Node.i += 1
        return Node.i

class BinOp(Node):

    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.i = Node.newId()

    def Evaluate(self, symbolTable, compiler):
        c1 = self.children[0].Evaluate(symbolTable, compiler)
        compiler.add("PUSH EBX \n")
        c2 = self.children[1].Evaluate(symbolTable, compiler)
        # print(c1, c2, self.value)
        result = None
        # if (c1[1] == "String" or c2[1] == "String") and not(self.value == "TIMES" or self.value == "EQUALS"):
        #     raise Exception("Invalid String Operation")
        compiler.add("POP EAX \n")
        if self.value == "PLUS" or self.value == "MINUS" or self.value == "TIMES" or self.value == "DIVIDED":
            if c1[1] == "Bool":
                c1 = (int(c1[0]), c1[1])
            if c2[1] == "Bool":
                c2 = (int(c2[0]), c2[1])

            if self.value == "PLUS":
                result = (c1[0] + c2[0], "Int")
                compiler.add("ADD EAX, EBX \n")

            elif self.value == "MINUS":
                result = (c1[0] - c2[0], "Int")
                compiler.add("SUB EAX, EBX \n")

            elif self.value == "TIMES":
                # if c1[1] == "String" or c2[1] == "String":
                #     result = (str(c1[0]) + str(c2[0]), "String")
                # else:
                result = (c1[0] * c2[0], "Int")
                compiler.add("IMUL EBX \n")

            elif self.value == "DIVIDED":
                result = (int(c1[0] / c2[0]), "Int")
                compiler.add("IDIV EBX \n")
        else:
            if c1[1] == "Int" and (self.value == "OR" or self.value =="AND"):
                c1 = (c1[0] != 0, c1[1])
            if c2[1] == "Int"and (self.value == "OR" or self.value =="AND"):
                c2 = (c2[0] != 0, c2[1])

            if self.value == "GREATER":
                result = (c1[0] > c2[0], "Bool")
                compiler.add("CMP EAX, EBX \n")
                compiler.add("CALL binop_jg \n")

            elif self.value == "LESS":
                result = (c1[0] < c2[0], "Bool")
                compiler.add("CMP EAX, EBX \n")
                compiler.add("CALL binop_jl \n")

            elif self.value == "EQUALS":
                # if c1[1] == "String" or c2[1] == "String":
                #     if c1[1] != c2[1]:
                #         raise Exception("Invalid String Operation")
                result = (c1[0] == c2[0], "Bool")
                compiler.add("CMP EAX, EBX \n")
                compiler.add("CALL binop_je \n")

            elif self.value == "AND":
                result = (bool(c1[0] and c2[0]), "Bool")
                compiler.add("AND EAX, EBX \n")

            elif self.value == "OR":
                result = (bool(c1[0] or c2[0]), "Bool")
                compiler.add("OR EAX, EBX \n")

        if self.value != "GREATER" and self.value != "LESS" and self.value != "EQUALS":
            compiler.add("MOV EBX, EAX \n")

        return result


class UnOp(Node):

    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.i = Node.newId()

    def Evaluate(self, symbolTable, compiler):
        c = self.children[0].Evaluate(symbolTable, compiler)
        result = None
        # if c[1] == "String":
        #     raise Exception("Invalid String Operation")
        if self.value == "PLUS":
            if c[1] == "Bool":
                c = (int(c[0]), c[1])
            result = (1 * c[0], "Int")
            

        elif self.value == "MINUS":
            if c[1] == "Bool":
                c = (int(c[0]), c[1])
            result = (-1 * c[0], "Int")
            compiler.add("NEG EBX \n")

        elif self.value == "NOT":
            if c[1] == "Int":
                c = (c[0] != 0, c[1])
            result = (bool(not c[0]), "Bool")
            compiler.add("NOT EBX \n")

        return result


class IntVal(Node):

    def __init__(self, value):
        self.value = value
        self.children = []
        self.i = Node.newId()

    def Evaluate(self, symbolTable, compiler):
        compiler.add("MOV EBX, {} \n".format(self.value))
        return (self.value, "Int")


class BoolVal(Node):
    def __init__(self, value):
        self.value = value
        self.children = []
        self.i = Node.newId()

    def Evaluate(self, symbolTable, compiler):
        compiler.add("MOV EBX, {} \n".format(self.value))
        return (self.value, "Bool")


# class StringVal(Node):
#     def __init__(self, value):
#         self.value = value
#         self.children = []
#         self.i = Node.newId()

#     def Evaluate(self, symbolTable, compiler):
#         return (self.value, "String")


class NoOp(Node):

    def Evaluate(self, symbolTable, compiler):
        pass


class Println(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.i = Node.newId()

    def Evaluate(self, symbolTable, compiler):
        print(self.children[0].Evaluate(symbolTable, compiler)[0])
        # self.children[0].Evaluate(symbolTable, compiler)
        compiler.add("PUSH EBX \n")
        compiler.add("CALL print \n")
        compiler.add("POP EBX \n")


class Statements(Node):
    def __init__(self):
        self.value = "BLOCK"
        self.children = []
        self.i = Node.newId()

    def Evaluate(self, symbolTable, compiler):
        for child in self.children:
            child.Evaluate(symbolTable, compiler)


class Identifier(Node):
    def __init__(self, value):
        self.value = value
        self.children = []
        self.i = Node.newId()

    def Evaluate(self, symbolTable, compiler):
        var = symbolTable.getVar(self.value)
        compiler.add("MOV EBX, [EBP-{}] \n".format(var[2] * 4))

        return (var[0], var[1])


class Assignment(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.i = Node.newId()

    def Evaluate(self, symbolTable, compiler):
        symbolTable.setVar(
            self.children[0].value, self.children[1].Evaluate(symbolTable, compiler))
        var = symbolTable.getVar(self.children[0].value)
        compiler.add("MOV [EBP-{}], EBX \n".format(var[2] * 4))


# class ReadLine(Node):
#     def __init__(self):
#         self.value = None
#         self.children = []
#         self.i = Node.newId()

#     def Evaluate(self, symbolTable, compiler):
#         readLine = int(input())
#         self.value = readLine
#         return (self.value, "Int")


class While(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.i = Node.newId()

    def Evaluate(self, symbolTable, compiler):
        compiler.add("LOOP_{}: \n".format(self.i))
        self.children[0].Evaluate(symbolTable, compiler)
        compiler.add("CMP EBX, False \n")
        compiler.add("JE EXIT_{} \n".format(self.i))
        self.children[1].Evaluate(symbolTable, compiler)
        compiler.add("JMP LOOP_{} \n".format(self.i))
        compiler.add("EXIT_{}: \n".format(self.i))

class If(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.i = Node.newId()

    def Evaluate(self, symbolTable, compiler):
        self.children[0].Evaluate(symbolTable, compiler)
        compiler.add("CMP EBX, False \n")
        compiler.add("JE EXIT_{} \n".format(self.i))
        self.children[1].Evaluate(symbolTable, compiler)
        compiler.add("JMP ENDIF_{} \n".format(self.i))
        compiler.add("EXIT_{}: \n".format(self.i))
        if len(self.children) == 3:
            self.children[2].Evaluate(symbolTable, compiler)
        compiler.add("ENDIF_{}: \n".format(self.i))


class DeclareVar(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.i = Node.newId()

    def Evaluate(self, symbolTable, compiler):
        compiler.add("PUSH DWORD 0 \n")
        symbolTable.declareVar(self.children[0].value, self.children[1].Evaluate(symbolTable, compiler))


class Type(Node):
    def __init__(self, value):
        self.value = value
        self.children = []
        self.i = Node.newId()

    def Evaluate(self, symbolTable, compiler):
        return self.value