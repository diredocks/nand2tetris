(KB)

@SCREEN
D=A
@current_word
M=D

@KBD
D=M
@NOT_PRESSED
D;JEQ
@PRESSED
D;JNE

(NOT_PRESSED)

(LOOP_NPSD)

@KBD
D=A
@current_word
D=M-D // current_word-KBD
@KB
D;JEQ

@current_word
A=M
M=0
@current_word
M=M+1

@LOOP_NPSD
0;JMP

(PRESSED)

(LOOP_PSD)

@KBD
D=A
@current_word
D=M-D // current_word-KBD
@KB
D;JEQ

@current_word
A=M
M=-1
@current_word
M=M+1

@LOOP_PSD
0;JMP
