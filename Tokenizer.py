import Token as tk

class Tokenizer:

    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None
        self.reserved = ["println"]

    def selectNext(self):
        if self.position < len(self.origin):
            current = self.origin[self.position]
            if current == " ":
                while self.origin[self.position] == " ":
                    self.position += 1
                    if self.position == len(self.origin):
                        self.actual = tk.Token("EOF", "")
                        return
                current = self.origin[self.position]
            #print(current)
            if current == "+":
                self.actual = tk.Token("PLUS", "+")
                self.position += 1

            elif current == "-":
                self.actual = tk.Token("MINUS", "-")
                self.position += 1
            
            elif current == "*":
                self.actual = tk.Token("TIMES", "*")
                self.position += 1

            elif current == "/":
                self.actual = tk.Token("DIVIDED", "/")
                self.position += 1
            
            elif current == "(":
                self.actual = tk.Token("OPEN", "(")
                self.position += 1
            elif current == ")":
                self.actual = tk.Token("CLOSE", ")")
                self.position += 1
            
            elif (current == "="):
                # print("igual")
                self.actual = tk.Token("ASSIGNMENT", "=")
                self.position += 1

            elif (current == "\n"):
                self.actual = tk.Token("ENDLINE", "\n")
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

            elif current.isalnum() and not current.isdigit():
                counter = 1
                command = "" + current
                if self.position < len(self.origin) - 1:
                    nextLet = self.origin[self.position + 1]
                    while (nextLet.isalnum() or nextLet == "_" or nextLet.isdigit()):
                        command += nextLet
                        counter += 1
                        if self.position+counter < len(self.origin):
                            nextLet = self.origin[self.position+counter]
                        else:
                            break
                if command in self.reserved:
                    self.actual = tk.Token("RESERVED", command)
                else:
                    self.actual = tk.Token("VARIABLE", command)
                self.position += counter

            else:
                raise Exception("Token invalido")
        else:
            self.actual = tk.Token("EOF", "")


