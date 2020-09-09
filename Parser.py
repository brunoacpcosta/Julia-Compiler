import Tokenizer as tkr

class Parser:
    tokens = None

    @staticmethod
    def parseExpression():
        result = Parser.parseTerm()
        current = Parser.tokens.actual
        #print(current.value)
        while (current.type == "PLUS" or current.type == "MINUS") and current.type != "EOF":

            if current.type == "PLUS":
                Parser.tokens.selectNext()
                result += Parser.parseTerm()
                current = Parser.tokens.actual

            elif current.type == "MINUS":
                Parser.tokens.selectNext()
                result -= Parser.parseTerm()
                current = Parser.tokens.actual

        return result


    @staticmethod
    def parseTerm():
        result = Parser.parseFactor()
        #print(result)
        current = Parser.tokens.actual
        #print(current.type)
        while (current.type == "TIMES" or current.type == "DIVIDED") and current.type != "EOF":
            if current.type == "TIMES":
                Parser.tokens.selectNext()
                result = result * Parser.parseFactor()
                current = Parser.tokens.actual

            elif current.type == "DIVIDED":
                Parser.tokens.selectNext()
                result = int(result / Parser.parseFactor())
                current = Parser.tokens.actual

        return result


    @staticmethod
    def parseFactor():
        current = Parser.tokens.actual
        #print(current.value)
        #print(current.type)
        if current.type == "PLUS":
            Parser.tokens.selectNext()
            result = Parser.parseFactor()
            current = Parser.tokens.actual

        elif current.type == "MINUS":
            Parser.tokens.selectNext()
            result = -1 * Parser.parseFactor()
            current = Parser.tokens.actual

        elif current.type == "INT":
            Parser.tokens.selectNext()
            result = current.value
            current = Parser.tokens.actual

        
        elif current.type == "OPEN":
            Parser.tokens.selectNext()
            result = Parser.parseExpression()
            #print(result)
            current = Parser.tokens.actual
           #print(current.value)
            if current.type != "CLOSE":
                raise Exception("Nao fechou parenteses")
            Parser.tokens.selectNext()
            
        else:
            #print(current.type)
            raise Exception("Token invalido no Parse Factor")
        return result
    
    @staticmethod
    def run(code):
        Parser.tokens= tkr.Tokenizer(code)
        Parser.tokens.selectNext()
        result = Parser.parseExpression()
        if Parser.tokens.actual.type == "EOF":
            return result
        else:
            #print(Parser.tokens.actual.type)
            raise Exception("Tokenizer nao chegou no EOF")


