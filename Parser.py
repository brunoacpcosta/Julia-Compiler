import Node as n
import Tokenizer as tkr

class Parser:
    tokens = None

    @staticmethod
    def parseExpression():
        node = Parser.parseTerm()
        current = Parser.tokens.actual
        while (current.type == "PLUS" or current.type == "MINUS") and current.type != "EOF":

            if current.type == "PLUS":
                Parser.tokens.selectNext()
                term = Parser.parseTerm()
                node = n.BinOp("PLUS", [node, term])
                current = Parser.tokens.actual

            elif current.type == "MINUS":
                Parser.tokens.selectNext()
                term = Parser.parseTerm()
                node = n.BinOp("MINUS", [node, term])
                current = Parser.tokens.actual

        return node


    @staticmethod
    def parseTerm():
        node = Parser.parseFactor()
        current = Parser.tokens.actual
        while (current.type == "TIMES" or current.type == "DIVIDED") and current.type != "EOF":

            if current.type == "TIMES":
                Parser.tokens.selectNext()
                factor = Parser.parseFactor()
                node = n.BinOp("TIMES", [node, factor])
                current = Parser.tokens.actual

            elif current.type == "DIVIDED":
                Parser.tokens.selectNext()
                factor = Parser.parseFactor()
                node = n.BinOp("DIVIDED", [node, factor])
                current = Parser.tokens.actual

        return node


    @staticmethod
    def parseFactor():
        current = Parser.tokens.actual
        if current.type == "PLUS":
            Parser.tokens.selectNext()
            factor = Parser.parseFactor()
            node = n.UnOp("PLUS", [factor])
            current = Parser.tokens.actual

        elif current.type == "MINUS":
            Parser.tokens.selectNext()
            factor = Parser.parseFactor()
            node = n.UnOp("MINUS", [factor])
            current = Parser.tokens.actual

        elif current.type == "INT":
            node = n.IntVal(current.value)
            Parser.tokens.selectNext()
            current = Parser.tokens.actual

        
        elif current.type == "OPEN":
            Parser.tokens.selectNext()
            node = Parser.parseExpression()
            current = Parser.tokens.actual
            if current.type != "CLOSE":
                raise Exception("Nao fechou parenteses")
            Parser.tokens.selectNext()

        elif current.type == "VARIABLE":
            node = n.Identifier(current.value)
            Parser.tokens.selectNext()
            current = Parser.tokens.actual
            
        else:
            raise Exception("Queria FACTOR, recebeu {}".format(current.type))
        return node


    @staticmethod
    def parseCommand():
        current = Parser.tokens.actual
        if (current.type == "VARIABLE"):
            var = n.Identifier(current.value)
            Parser.tokens.selectNext()
            current = Parser.tokens.actual
            if (current.type == "ASSIGNMENT"):
                Parser.tokens.selectNext()
                current = Parser.tokens.actual
                exp = Parser.parseExpression()
                node = n.Assignment("ASSIGNMENT", [var, exp])
                current = Parser.tokens.actual
                if (current.type == "ENDLINE" or current.type == "EOF"):
                    Parser.tokens.selectNext()
                    current = Parser.tokens.actual
                    return node
                else:
                   raise Exception("Queria ENDLINE, recebeu {}".format(current.type))
            else:
                raise Exception("Queria ASSIGNMENT, recebeu {}".format(current.type))

        elif (current.type == "RESERVED"):
            if (current.value == "println"):
                Parser.tokens.selectNext()
                current = Parser.tokens.actual
                if (current.type == "OPEN"):
                    Parser.tokens.selectNext()
                    exp = Parser.parseExpression()
                    
                    node = n.Println("PRINT", [exp])
                    current = Parser.tokens.actual
                    if (current.type == "CLOSE"):
                        Parser.tokens.selectNext()
                        current = Parser.tokens.actual
                        if (current.type == "ENDLINE" or current.type == "EOF"):
                            Parser.tokens.selectNext()
                            current = Parser.tokens.actual
                            return node
                        else:
                            raise Exception("Queria ENDLINE, recebeu {}".format(current.type))
                    else:
                        raise Exception("Queria CLOSE, recebeu {}".format(current.type))
                else:
                    raise Exception("Queria OPEN, recebeu {}".format(current.type))
                
            else:
                raise Exception("Queria println, recebeu {}".format(current.value))

        elif (current.type == "ENDLINE" or current.type == "EOF"):
            Parser.tokens.selectNext()
            return n.NoOp()

        else:
            raise Exception("Queria ENDLINE - final, recebeu {}".format(current.type))

        
    @staticmethod
    def parseBlock():
        current = Parser.tokens.actual
        block = n.Block()
        while (current.type != "EOF"):
            block.children.append(Parser.parseCommand())
            current = Parser.tokens.actual
        return block

    @staticmethod
    def run(code):
        Parser.tokens = tkr.Tokenizer(code)
        Parser.tokens.selectNext()
        node = Parser.parseBlock()
        if Parser.tokens.actual.type == "EOF":
            return node
        else:
            #print(Parser.tokens.actual.type)
            raise Exception("Tokenizer nao chegou no EOF")


