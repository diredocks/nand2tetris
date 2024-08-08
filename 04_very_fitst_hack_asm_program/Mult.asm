@sum
M=0
@i
M=0

(LOOP)
// x*y = x+x+...+x for y times
@i
M=M+1 // i++
D=M

@R1
D=M-D // y-i
@END
D;JLT

@R0
D=M
@sum
M=D+M

@LOOP
0;JMP

(END)
@sum
D=M
@R2
M=D
@0
0;JMP
