        ORG 0000H
        SJMP MAIN
        ORG 0003H
        LJMP LEFTOB
        ORG 0013H
        LJMP RIGHTOB
        
MAIN    MOV IE,#85H   ;Enable External Interrupts  

        MOV R2,#0EH   ;Load Register r2 with 1F(outer 8 bit repeater loop)
LOOP    ACALL DELAY   ;Call Delay Subroutine  
        ACALL FORWARD ;Call Forward Subroutine

DELAY   MOV TMOD,#01H ;Configure Timer Control for Timer 0 mode 1
        MOV TH0,#00H  ;Load high order 8 bit 
        MOV TL0,#00H  ;Load low order 8 bit 
        SETB TR0      ;Start Timer
AGAIN   JNB TF0,AGAIN ;Check for Timer Flag
        CLR TF0       ;Clear timer flag
        CLR TR0       ;clear timer Register
        DJNZ R2,DELAY ;Decrement register R2 and jump if non-zero
        RET           ;Return to main Program

FORWARD MOV P2,#0B8H  ;Forward Motion
        SJMP FORWARD       

LEFTOB  MOV IE,#00H   ;Disable all Interrupts
        MOV P2,#0FCH  ;Forceful Stop
        MOV P2,#02H   ;Rotate Camera

        MOV R2,#014H  ;Delay 
        ACALL DELAY   ;Call Delay Subroutine

        MOV P2,#0D4H  ;Reverse Motors

        MOV R2,#01CH  ;Delay 
        ACALL DELAY   ;Call Delay Subroutine

        MOV P2,#0FCH  ;Forceful Stop
        MOV P2,#02H   ;Rotate Camera

        MOV R2,#15H   ;Delay
        ACALL DELAY   ;Call Delay Subroutine

        MOV P2,#0BCH  ;Rotate Left Motor 

        MOV R2,#01CH  ;Delay
        ACALL DELAY   ;Call Delay Subroutine

        MOV P2,#0FCH  ;Forceful Stop
        MOV P2,#02H   ;Rotate Camera

        MOV R2,#01FH  ;Delay
        ACALL DELAY   ;Call Delay Subroutine	
         
        MOV P2,#00H   ;Clear Outputs

        MOV R2,#04H   ;Delay
        ACALL DELAY   ;Call Delay Subroutine 
         
        MOV IE,#85H   ;Enable All Interrupts
        RETI

RIGHTOB MOV IE,00H    ;Disable All Interrupts
        MOV P2,#0FCH  ;Forceful Stop
        MOV P2,#02H   ;Rotate Camera

        MOV R2,#12H   ;Delay
        ACALL DELAY   ;Call Delay Subroutine

        MOV P2,#0D4H  ;Reverse Motors

        MOV R2,#01CH  ;Delay
        ACALL DELAY   ;Call Delay Subroutine 

        MOV P2,#0FCH  ;Forceful Stop
        MOV P2,#02H   ;Rotate Camera

        MOV R2,#0EH   ;Delay
        ACALL DELAY   ;Call Delay Subroutine 
        
        MOV P2,#0F8H  ;Rotate Right Motor

        MOV R2,#1CH   ;Delay
        ACALL DELAY   ;Call Delay Subroutine 

        MOV P2,#0FCH  ;Forceful Stop
        MOV P2,#02H   ;Rotate Camera

        MOV R2,#07H   ;Delay
        ACALL DELAY   ;Call Delay Subroutine 

        MOV P2,#00H   ;Clear Outputs

        MOV R2,#0EH   ;Delay 
        ACALL DELAY   ;Call Delay Subroutine

        MOV IE,#85H   ;Enable All Interrupts
        RETI
