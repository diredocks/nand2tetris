# Arithmetic / Logical Commands in Stack Machine

Each command should first move the selected memory to where
register '*sp'(stack pointer) pointed to.

This could be done by the following Hack ASM command:
`@SP;A=M`
R0 is where SP lies

## Operations
### With two operator
For two operator, it should first read the last operator into
register 'D', with `A=A-1;D=M`

Then it reads the first operator and calculate in place with
`A=A-1;M=M(op)D`, where `(op)` refers to the operations applied
to these two operators.

1. add
2. sub
3. and
4. or

5. eq
6. gt
7. lt

After the operation, move pointer to the stack head and put the
head head postision to register '*sp'.
`D=A+1;@SP;M=D`


## ops
push seg n -> push data n from seg into stack
pop  seg n -> pop  data n from stack into seg

```asm
@SP
A=M-1
D=M
A=A-1
M=M-D // calc A-B

D=A+1
@SP
M=D // save result into stack

A=D-1 // jump to result

D=M
@eq
D;JEQ
// if not eq
@SP
A=M-1
M=0
@ed
0;JMP

(eq)
@SP
A=M-1
M=1
@ed
0;JMP

(ed) // if we would like to do it twice or mroe
// we need a lable suffixed with number
```
