# Arithmetic / Logical Commands in a Stack Machine
## General Operation Flow

Move Memory to Stack: Each command should first move the selected memory to the location pointed to by the stack pointer (*sp).
This can be done using the following Hack ASM command:

```asm
@SP
A=M
```

Note: SP (stack pointer) resides in R0.

## Arithmetic/Logical Operations
### For Operations with Two Operands

For binary operations (those requiring two operands):

Load the second operand: Load the last operand on the stack into register D using:

```asm
A=A-1
D=M
```

Apply the operation: Load the first operand and perform the operation in place with:

```asm
A=A-1
M=M(op)D
```

where (op) refers to the operation applied (e.g., + for addition, - for subtraction).

### Supported Operations

1. add (+)
2. sub (-)
3. and (&)
4. or (|)

### Comparison Operations

1. eq (equal, ==)
2. gt (greater than, >)
3. lt (less than, <)

## After Operation: Update Stack Pointer

After performing the operation:

Move the pointer to the top of the stack and update the stack pointer register:

```
D=A+1
@SP
M=D
```
## Example: Equality Check (eq)

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
M=-1
(ed)
```

## Stack Operations
push seg n: Push the value from segment seg at index n onto the stack.
pop seg n: Pop the value from the stack and store it into segment seg at index n.

Notes:

When working with comparisons like eq, gt, or lt, ensure the use of conditional jumps (e.g., JEQ for equality, JGT for greater than, JLT for less than).

If you'd like to perform the same operation multiple times or need multiple labels, consider suffixing labels with numbers (e.g., eq1, eq2, etc.) for uniqueness.
