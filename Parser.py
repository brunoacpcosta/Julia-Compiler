import Tokenizer as tkr

class Parser:

    def parseExpression(self):
        result = 0
        self.tokens.selectNext()
        current = self.tokens.actual
        #print(current.value)

        if current.type == "INT":
            result = current.value
            self.tokens.selectNext()
            current = self.tokens.actual
            #print(current.value)
            while (current.type == "PLUS" or current.type == "MINUS") and current.type != "EOF":

                if current.type == "PLUS":
                    self.tokens.selectNext()
                    current = self.tokens.actual
                    #print(current.value)
                    if current.type == "INT":
                        result += current.value

                    else:
                        raise Exception("Soma sem Numero depois")

                elif current.type == "MINUS":
                    self.tokens.selectNext()
                    current = self.tokens.actual
                    #print(current.value)
                    if current.type == "INT":
                        result -= current.value

                    else:
                        raise Exception("Subtracao sem Numero depois")
                    
                self.tokens.selectNext()
                current = self.tokens.actual
                #print(current.value)

            return result
        else:
            raise Exception("Expressao nao comeca com numero")

    def run(self, code):
        self.tokens = tkr.Tokenizer(code)
        result = self.parseExpression()
        #print("=")
        print(result)
