SYS_EXIT equ 1 
SYS_READ equ 3 
SYS_WRITE equ 4 
STDIN equ 0 
STDOUT equ 1 
True equ 1 
False equ 0 
segment .data 
segment .bss 
res RESB 1 
section .text 
global _start 
print:  ; subrotina print 
PUSH EBP ; guarda o base pointer 
MOV EBP, ESP ; estabelece um novo base pointer 
MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP 
XOR ESI, ESI 
print_dec: ; empilha todos os digitos 
MOV EDX, 0 
MOV EBX, 0x000A 
DIV EBX 
ADD EDX, '0' 
PUSH EDX 
INC ESI ; contador de digitos 
CMP EAX, 0 
JZ print_next ; quando acabar pula 
JMP print_dec 
print_next: 
CMP ESI, 0 
JZ print_exit ; quando acabar de imprimir 
DEC ESI 
MOV EAX, SYS_WRITE 
MOV EBX, STDOUT 
POP ECX 
MOV [res], ECX 
MOV ECX, res 
MOV EDX, 1 
INT 0x80 
JMP print_next 
print_exit: 
POP EBP 
RET 
; subrotinas if/while 
binop_je: 
JE binop_true 
JMP binop_false 
binop_jg: 
JG binop_true 
JMP binop_false 
binop_jl: 
JL binop_true 
JMP binop_false 
binop_false: 
MOV EBX, False 
JMP binop_exit 
binop_true: 
MOV EBX, True 
binop_exit: 
RET 
_start: 
PUSH EBP ; guarda o base pointer 
MOV EBP, ESP ; estabelece um novo base pointer 
PUSH DWORD 0 
PUSH DWORD 0 
PUSH DWORD 0 
PUSH DWORD 0 
MOV EBX, 5 
MOV [EBP-4], EBX 
MOV EBX, 0 
MOV [EBP-8], EBX 
MOV EBX, 10 
MOV [EBP-12], EBX 
LOOP_31: 
MOV EBX, [EBP-8] 
PUSH EBX 
MOV EBX, 5 
POP EAX 
CMP EAX, EBX 
CALL binop_jl 
PUSH EBX 
MOV EBX, [EBP-8] 
PUSH EBX 
MOV EBX, 5 
POP EAX 
CMP EAX, EBX 
CALL binop_je 
POP EAX 
OR EAX, EBX 
MOV EBX, EAX 
CMP EBX, False 
JE EXIT_31 
MOV EBX, [EBP-8] 
PUSH EBX 
MOV EBX, 3 
POP EAX 
CMP EAX, EBX 
CALL binop_jl 
CMP EBX, False 
JE EXIT_36 
MOV EBX, 2 
PUSH EBX 
CALL print 
POP EBX 
JMP ENDIF_36 
EXIT_36: 
MOV EBX, [EBP-8] 
PUSH EBX 
MOV EBX, 3 
POP EAX 
CMP EAX, EBX 
CALL binop_je 
CMP EBX, False 
JE EXIT_43 
MOV EBX, 20 
PUSH EBX 
CALL print 
POP EBX 
JMP ENDIF_43 
EXIT_43: 
MOV EBX, [EBP-8] 
PUSH EBX 
MOV EBX, 4 
POP EAX 
CMP EAX, EBX 
CALL binop_je 
CMP EBX, False 
JE EXIT_50 
MOV EBX, 200 
PUSH EBX 
CALL print 
POP EBX 
JMP ENDIF_50 
EXIT_50: 
MOV EBX, 2000 
PUSH EBX 
CALL print 
POP EBX 
ENDIF_50: 
ENDIF_43: 
ENDIF_36: 
MOV EBX, [EBP-8] 
PUSH EBX 
MOV EBX, 3 
POP EAX 
CMP EAX, EBX 
CALL binop_jg 
NOT EBX 
PUSH EBX 
MOV EBX, [EBP-12] 
PUSH EBX 
MOV EBX, 10 
POP EAX 
CMP EAX, EBX 
CALL binop_je 
POP EAX 
AND EAX, EBX 
MOV EBX, EAX 
CMP EBX, False 
JE EXIT_66 
MOV EBX, 10 
PUSH EBX 
CALL print 
POP EBX 
JMP ENDIF_66 
EXIT_66: 
MOV EBX, 100 
PUSH EBX 
CALL print 
POP EBX 
ENDIF_66: 
MOV EBX, [EBP-8] 
PUSH EBX 
MOV EBX, 3 
POP EAX 
CMP EAX, EBX 
CALL binop_jg 
PUSH EBX 
MOV EBX, [EBP-8] 
PUSH EBX 
MOV EBX, [EBP-12] 
POP EAX 
CMP EAX, EBX 
CALL binop_jl 
POP EAX 
AND EAX, EBX 
MOV EBX, EAX 
PUSH EBX 
CALL print 
POP EBX 
MOV EBX, [EBP-8] 
PUSH EBX 
CALL print 
POP EBX 
MOV EBX, [EBP-8] 
PUSH EBX 
MOV EBX, 1 
POP EAX 
ADD EAX, EBX 
MOV EBX, EAX 
MOV [EBP-8], EBX 
JMP LOOP_31 
EXIT_31: 
PUSH DWORD 0 
PUSH DWORD 0 
MOV EBX, 1 
MOV [EBP-20], EBX 
MOV EBX, True 
MOV [EBP-24], EBX 
MOV EBX, [EBP-20] 
PUSH EBX 
MOV EBX, [EBP-24] 
POP EAX 
ADD EAX, EBX 
MOV EBX, EAX 
PUSH EBX 
CALL print 
POP EBX 
POP EBP 
MOV EAX, 1 
INT 0x80