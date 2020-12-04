import Token as tk


class Tokenizer:

    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None
        self.reserved = ["println", "if", "else",
                         "while", "elseif", "end", "readline", "local", "true", "false", "global", "return", "function"]
        self.types = ["Int", "Bool", "String"]

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

            elif current == ">":
                self.actual = tk.Token("GREATER", ">")
                self.position += 1

            elif current == "<":
                self.actual = tk.Token("LESS", "<")
                self.position += 1

            elif current == "!":
                self.actual = tk.Token("NOT", "!")
                self.position += 1

            elif current == ",":
                self.actual = tk.Token("COMMA", ",")
                self.position += 1

            elif current == '"':
                counter = 1
                command = "" + current
                if self.position < len(self.origin) - 1:
                    nextLet = self.origin[self.position + 1]
                    while nextLet != '"':
                        command += nextLet
                        counter += 1
                        if self.position+counter < len(self.origin):
                            nextLet = self.origin[self.position+counter]
                        else:
                            raise Exception("String not closed")
                    self.actual = tk.Token("STRING", command[1:])
                    self.position += (counter + 1)

            elif current == "=":
                if self.origin[self.position+1] == "=":
                    self.actual = tk.Token("EQUALS", "==")
                    self.position += 2
                else:
                    self.actual = tk.Token("ASSIGNMENT", "=")
                    self.position += 1

            elif current == "|":
                if self.origin[self.position+1] == "|":
                    self.actual = tk.Token("OR", "||")
                    self.position += 2
                else:
                    raise Exception("Queria OR, recebeu {}".format("|" +
                        self.origin[self.position+1]))

            elif current == ":":
                if self.origin[self.position+1] == ":":
                    self.actual = tk.Token("DECLARE", "::")
                    self.position += 2
                else:
                    raise Exception("Queria DECLARE, recebeu {}".format(":" +
                        self.origin[self.position+1]))

            elif current == "&":
                if self.origin[self.position+1] == "&":
                    self.actual = tk.Token("AND", "&&")
                    self.position += 2
                else:
                    raise Exception("Queria AND, recebeu {}".format("&" +
                        self.origin[self.position+1]))

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
                if command in self.types:
                    self.actual = tk.Token("TYPE", command)

                elif command in self.reserved:
                    if (command == "true" or command == "false"):
                        self.actual = tk.Token("BOOL", command)
                    else:
                        self.actual = tk.Token("RESERVED", command)
                else:
                    self.actual = tk.Token("VARIABLE", command)
                self.position += counter

            else:
                raise Exception("Queria TOKEN, recebeu {}".format(current))
        else:
            self.actual = tk.Token("EOF", "")

        # print("Type: {}     Value: {}".format(self.actual.type, self.actual.value))
