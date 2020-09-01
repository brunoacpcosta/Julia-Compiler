import Tokenizer as tkr

class Parser:
    tokens = None
    @staticmethod
    def parseExpression():
        result = 0
        Parser.tokens.selectNext()
        current = Parser.tokens.actual
        #print(current.value)

        if current.type == "INT":
            result = current.value
            Parser.tokens.selectNext()
            current = Parser.tokens.actual
            #print(current.value)
            while (current.type == "PLUS" or current.type == "MINUS" or current.type == "TIMES" or current.type == "DIVIDED") and current.type != "EOF":
 
                if current.type == "PLUS":
                    Parser.tokens.selectNext()
                    current = Parser.tokens.actual
                    #print(current.value)
                    if current.type == "INT":
                        result += current.value

                    else:
                        raise Exception("Soma sem Numero depois")

                elif current.type == "MINUS":
                    Parser.tokens.selectNext()
                    current = Parser.tokens.actual
                    #print(current.value)
                    if current.type == "INT":
                        result -= current.value

                    else:
                        raise Exception("Subtracao sem Numero depois")

                elif current.type == "TIMES":
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
            raise Exception("Expressao nao comeca com numero")
    
    @staticmethod
    def run(code):
        Parser.tokens= tkr.Tokenizer(code)
        result = Parser.parseExpression()
        #print("=")
        print(result)
