/*********************************************************************************
* This program demonstrates use of POLLING with assembly language code.
*
* The program continously reads the pushbutton KEY port in the FPGA and
* indicates which KEY has been pressed on the HEX0 display.
*
********************************************************************************/

.equ LED_BASE, 0xff200000
.equ SWITCHES_BASE, 0xff200040
.equ PUSH_BUTTONS_BASE, 0xff200050
.equ DISPLAYS_BASE, 0xff200020

.global _start
_start:
    B LOOP

LOOP:
    // Read push buttons
	LDR r0, =PUSH_BUTTONS_BASE
	LDR r1, [r0]

	// Check and display
	LDR r0, =DISPLAYS_BASE
CHECK_KEY0:
	ANDS r3, r1, #0b00000001
	BEQ CHECK_KEY1
	MOV r2, #0b00111111
	STR r2, [r0]	// display "0"
	B LOOP
	
CHECK_KEY1:
	ANDS r3, r1, #0b00000010
	BEQ CHECK_KEY2
	MOV r2, #0b00000110
	STR r2, [r0]	// display "1"
	B LOOP

CHECK_KEY2:
	ANDS r3, r1, #0b00000100
	BEQ CHECK_KEY3
	MOV r2, #0b01011011
	STR r2, [r0]	// display "2"
	B LOOP

CHECK_KEY3:
	ANDS r3, r1, #0b00001000
	BEQ LOOP
	MOV r2, #0b01001111
	STR r2, [r0]	// display "3"
	B LOOP

.end
	
