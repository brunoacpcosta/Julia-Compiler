import Tokenizer as tkr

class Parser:
    tokens = None

    @staticmethod
    def parseExpression():
        result = Parser.parseTerm()
        current = Parser.tokens.actual
        while (current.type == "PLUS" or current.type == "MINUS") and current.type != "EOF":

            if current.type == "PLUS":
                result += Parser.parseTerm()
                current = Parser.tokens.actual

            elif current.type == "MINUS":
                result -= Parser.parseTerm()
                current = Parser.tokens.actual



        return result


    @staticmethod
    def parseTerm():
        result = 0
        Parser.tokens.selectNext()
        current = Parser.tokens.actual
        #print(current.value)
        print(current.type)
        if current.type == "INT":
            result = current.value
            Parser.tokens.selectNext()
            current = Parser.tokens.actual
            #print(current.value)
            while (current.type == "TIMES" or current.type == "DIVIDED") and current.type != "EOF":
 
                if current.type == "TIMES":
                    Parser.tokens.selectNext()
                    current = Parser.tokens.actual
                    #print(current.value)
                    if current.type == "INT":
                        result = current.value * result

                    else:
                        raise Exception("Multiplicacao sem Numero depois")
                
                elif current.type == "DIVIDED":
                    Parser.tokens.selectNext()
                    current = Parser.tokens.actual
                    #print(current.value)
                    if current.type == "INT":
                        result = result/current.value

                    else:
                        raise Exception("Divisao sem Numero depois")

                Parser.tokens.selectNext()
                current = Parser.tokens.actual
                #print(current.value)

            return result
        else:
            raise Exception("Nao e Numero")
    
    @staticmethod
    def run(code):
        Parser.tokens= tkr.Tokenizer(code)
        result = Parser.parseExpression()
        if Parser.tokens.actual.type == "EOF":
            return result
        else:
            raise Exception("Tokenizer nao chegou no EOF")


