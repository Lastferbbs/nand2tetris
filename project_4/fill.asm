// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

(START)
@KBD
D=A
@screen_size
M=D
@SCREEN
D=A
@addr
M=D
@screen_size
M=M-D
D=M
@R0
M=-1
@KBD
D=M
@CLEAR
D;JEQ
@FILL
D;JGT

(FILL)
@screen_size
D=M
@START
D;JEQ
@R0
D=M
@addr
A=M
M=D
@addr
M=M+1
@screen_size
M=M-1
@FILL
0;JMP

(CLEAR)
@R0
M=0
@FILL
0;JMP
