import Node as n
import Tokenizer as tkr

class Parser:
    tokens = None

    @staticmethod
    def parseExpression():
        node = Parser.parseTerm()
        current = Parser.tokens.actual
        # print(current.value)
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
        # print(current.type)
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
        # print(current.value)
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
            #print(result)
            current = Parser.tokens.actual
           #print(current.value)
            if current.type != "CLOSE":
                raise Exception("Nao fechou parenteses")
            Parser.tokens.selectNext()
            
        else:
            #print(current.type)
            raise Exception("Token invalido no Parse Factor")
        return node
    
    @staticmethod
    def run(code):
        Parser.tokens= tkr.Tokenizer(code)
        Parser.tokens.selectNext()
        node = Parser.parseExpression()
        if Parser.tokens.actual.type == "EOF":
            return node
        else:
            #print(Parser.tokens.actual.type)
            raise Exception("Tokenizer nao chegou no EOF")


