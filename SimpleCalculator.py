import math


class Token:

    def __init__(self, string, value):
        self.type = string
        self.value = value


class Tokenizer:

    def __init__(self, origin):
        origin = origin.replace(" ", "")
        self.origin = origin
        self.position = 0

    def selectNext(self):
        current = self.origin[self.position]
        if current == "+":
            self.actual = Token("PLUS", "+")
            self.position += 1

        elif current == "-":
            self.actual = Token("MINUS", "-")
            self.position += 1

        elif current.isnumeric():
            counter = 1
            list_nums = [current]
            if self.position < len(self.origin)-1:
                nextNum = self.origin[self.position+1]
                while nextNum.isnumeric():
                    list_nums.append(nextNum)
                    counter += 1
                    if self.position+counter < len(self.origin):
                        nextNum = self.origin[self.position+counter]
                    else:
                        break

            final = ""
            for i in list_nums:
                final += i

            final = int(final)
            self.actual = Token("INT", final)
            self.position += counter

        else:
            raise Exception("Token nao eh nem soma/subtracao, nem numero")


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
            while current.type == "PLUS" or current.type == "MINUS":

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
                if self.tokens.position < len(self.tokens.origin):
                    
                    self.tokens.selectNext()
                    current = self.tokens.actual
                    #print(current.value)

            return result
        else:
            raise Exception("Expressao nao comeca com numero")

    def run(self, code):
        self.tokens = Tokenizer(code)
        result = self.parseExpression()
        #print("=")
        print(result)


parser = Parser()
list_test = ["1+2", "3-2", "1+2-3", "11+22-33", "789     +345   -    123"]
for i in list_test:
    parser.run(i)
    print("-------")
