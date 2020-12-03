class Compiler():
    
    assembly = ["SYS_EXIT equ 1 \n",
            "SYS_READ equ 3 \n",
            "SYS_WRITE equ 4 \n",
            "STDIN equ 0 \n",
            "STDOUT equ 1 \n",
            "True equ 1 \n",
            "False equ 0 \n",
            "segment .data \n",
            "segment .bss \n",
            "res RESB 1 \n",

            "section .text \n",
            "global _start \n",

            "print:  ; subrotina print \n",

            "PUSH EBP ; guarda o base pointer \n",
            "MOV EBP, ESP ; estabelece um novo base pointer \n",

            "MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP \n",
            "XOR ESI, ESI \n",

            "print_dec: ; empilha todos os digitos \n",
            "MOV EDX, 0 \n",
            "MOV EBX, 0x000A \n",
            "DIV EBX \n",
            "ADD EDX, '0' \n",
            "PUSH EDX \n",
            "INC ESI ; contador de digitos \n",
            "CMP EAX, 0 \n",
            "JZ print_next ; quando acabar pula \n",
            "JMP print_dec \n",

            "print_next: \n",
            "CMP ESI, 0 \n",
            "JZ print_exit ; quando acabar de imprimir \n",
            "DEC ESI \n",

            "MOV EAX, SYS_WRITE \n",
            "MOV EBX, STDOUT \n",

            "POP ECX \n",
            "MOV [res], ECX \n",
            "MOV ECX, res \n",

            "MOV EDX, 1 \n",
            "INT 0x80 \n",
            "JMP print_next \n",

            "print_exit: \n",
            "POP EBP \n",
            "RET \n",

            "; subrotinas if/while \n",
            "binop_je: \n",
            "JE binop_true \n",
            "JMP binop_false \n",

            "binop_jg: \n",
            "JG binop_true \n",
            "JMP binop_false \n",

            "binop_jl: \n",
            "JL binop_true \n",
            "JMP binop_false \n",

            "binop_false: \n",
            "MOV EBX, False \n",
            "JMP binop_exit \n",
            "binop_true: \n",
            "MOV EBX, True \n",
            "binop_exit: \n",
            "RET \n",

            "_start: \n",

            "PUSH EBP ; guarda o base pointer \n",
            "MOV EBP, ESP ; estabelece um novo base pointer \n"
    ]
    @staticmethod
    def add(line):
        Compiler.assembly.append(line)

    @staticmethod
    def flush():
        Compiler.assembly.append("POP EBP \n")
        Compiler.assembly.append("MOV EAX, 1 \n")
        Compiler.assembly.append("INT 0x80")
        final = "".join(Compiler.assembly)
        print(final)
        with open("compiler.asm", "w") as codeFile:             
            codeFile.write(final)
        codeFile.close()
        return codeFile