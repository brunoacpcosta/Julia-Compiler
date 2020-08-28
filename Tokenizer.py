import Token as tk

class Tokenizer:

    def __init__(self, origin):
        origin = origin.replace(" ", "")
        origin = origin.replace("'", "")
        self.origin = origin
        self.position = 0

    def selectNext(self):
        if self.position < len(self.origin):
            current = self.origin[self.position]
            #print(current)
            if current == "+":
                self.actual = tk.Token("PLUS", "+")
                self.position += 1

            elif current == "-":
                self.actual = tk.Token("MINUS", "-")
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
                self.actual = tk.Token("INT", final)
                self.position += counter
            else:
                raise Exception("Token nao eh nem soma/subtracao, nem numero")
        else:
            self.actual = tk.Token("EOF", "")

