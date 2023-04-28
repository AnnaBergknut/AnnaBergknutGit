/******************************************************************************
    Define symbols
******************************************************************************/
// Proposed interrupt vector base address
.equ INTERRUPT_VECTOR_BASE, 0x00000000

// Proposed stack base addresses
.equ SVC_MODE_STACK_BASE, 0x3FFFFFFF - 3 // set SVC stack to top of DDR3 memory
.equ IRQ_MODE_STACK_BASE, 0xFFFFFFFF - 3 // set IRQ stack to A9 onchip memory

// GIC Base addresses
.equ GIC_CPU_INTERFACE_BASE, 0xFFFEC100
.equ GIC_DISTRIBUTOR_BASE, 0xFFFED000

// Other I/O device base addresses
.equ PUSH_BUTTON, 0xff200050
.equ SEVEN_DISPLAY, 0xff200020

/* Data section, for global data/variables if needed. */
.data
	numbers:
		.word 0x3f, 0x6, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x7, 0x7f, 0x67, 0x77, 0x7c, 0x39, 0x5e, 0x79, 0x71
    CurrentIndex:   .word 15

/* Code section */
.text

/*****************************************************************************
    Interrupt Vector
*****************************************************************************/
.org INTERRUPT_VECTOR_BASE  // Address of interrupt vector
// Write your Interrupt Vector here
.org 0x00000000  // Similar to .section above
B _start // reset vector
B SERVICE_UND // undefined instruction vector
B SERVICE_SVC // software interrrupt vector
B SERVICE_ABT_INST // aborted prefetch vector
B SERVICE_ABT_DATA // aborted data vector
.word 0 // unused vector
B SERVICE_IRQ // IRQ interrupt vector

.global _start
/*****************************************************************************************************
    System startup.
    ---------------

On system startup some basic configuration is needed, in this case:
    1. Setup stack pointers for each used processor mode
    2. Configure the Generic Interrupt Controller (GIC). Use the given help function CONFIG_GIC!
    3. Configure the used I/O devices and enable them for interrupt
    4. Change to the processor mode for the main program loop (for example supervisor mode)
    5. Enable the processor interrupts (IRQ in our case)
    6. Start running the main program loop

 Your program will use two different processor modes when running:
 -Supervisor mode (SVC) when running the main program loop. Also default mode on reset.
 -IRQ mode when handling IRQ interrupts

 Changing processor mode and/or enabling/disabling interrupts control bits
 is done by updating the program status register (CPSR) control bits [7:0]
 
 The CPSR register holds the processor mode control bits [4:0]:
   10011 - Supervisor mode (SVC)
   10010 - IRQ mode
 The CPSR register also holds the following interrupt control bits:
   bit [7] IRQ enable/disable. 0 means IRQ enabled, 1 means IRQ disabled
   bit [6] FIQ enable/disable. 0 means FIQ enabled, 1 means FIQ disabled
 Bit [5] of the CPSR register should always be 0 in this case!

 The instruction "MSR CPSR_c, #0b___" can be used to modify the CPSR control bits.
 Example: "MSR CPSR_c #0b11011111" diables both interrupts and sets processor mode to "system mode".

 The instruction "MRS CPSR_c, R__" can be used to read the CPSR control bits into a register.
 Example: "MRS CPSR_c R0" reads CPSR control bits for interrupts and processor mode into register R0.
*****************************************************************************************************/
// Write your system startup code here. Follow the steps in the description above!
_start:
//    MOV R1, #INT_DISABLE | IRQ_MODE
    MOV R1, #0b11010010 // interrupts masked, MODE = IRQ // irq = interupt request
    MSR CPSR_c, R1 // Change to IRQ mode. CPSR_c means only move the control bits [7:0] // move to system corissponder register
//    LDR SP, =A9_ONCHIP_END - 3  // set IRQ stack to top of A9 onchip memory
    LDR SP, =0xFFFFFFFF - 3 // set IRQ stack to A9 onchip memory // load rigister

    /* Change to SVC (supervisor) mode with interrupts disabled */
//    MOV R1, #INT_DISABLE | SVC_MODE
    MOV R1, #0b11010011 // interrupts masked, MODE = SVC // svc = supervise mode
    MSR CPSR_c, R1 // change to supervisor mode 
    LDR SP, =0x3FFFFFFF - 3 // set SVC stack to top of DDR3 memory
    MOV R0, #73 // push buttom key
    BL CONFIG_GIC   // configure the ARM generic interrupt controller
    BL CONFIG_PUSH_BUTTON // push button

    MOV R1, #0b01010011 // IRQ unmasked, MODE = SVC
    MSR CPSR_c, R1 // switches to SVC mode, enables interrupts to be handled while main program is running

/*******************************************************************
 Main program
*******************************************************************/
// Write code for your main program here
LOOP:
    B LOOP

CONFIG_PUSH_BUTTON: //om något förstörs pusha och poppa R1 
	PUSH {LR}
    LDR R1, =PUSH_BUTTON
    ADD R1, R1, #8
    MOV R3, #3
    STR R3, [R1]
	ADD R1, R1, #4
	STR R3, [R1]

	POP {PC} 

/*******************************************************************
    IRQ Interrupt Service Routine (ISR)
    -----------------------------------

The ISR  should:
    1. Read and acknowledge the interrupt at the GIC.The GIC returns the interrupt ID.
    2. Check which device raised the interrupt
    3. Handle the specific device interrupt
    4. Acknowledge the specific device interrupt
    5. Inform the GIC that the interrupt is handled
    6. Return from interrupt

The following GIC CPU interface registers should be used (both v2/v1 alternative names showed below):
    -Interrupt Acknowledge Register (GICC_IAR/ICCIAR)
        Reading this register returns the interrupt ID corresponding to the I/O device.
        This read acts as an acknowledge for the interrupt.
    -End of Interrupt Register (GICC_EOIR/ICCEOIR)
        Writing the corresponding interrupt ID to this register informs the GIC that
        the interrupt is handled and clears the interrupt from the GIC CPU interface.

How to handle a specific interrupt depends on the I/O device generating the interrupt.
Read the documentation for your I/O device carefully!
Every I/O device has a base address. Usually the I/O device has several registers
(32 bit words on a 32 bit architecture) starting from the base address. Each register, and 
often every bit in these registers, have a certain function and meaning. Look out for 
how to read and/write to your device and also how to enable/disable interrupts from the device.

Returning from an interrupt is done by using a special system level instruction:
    SUBS PC, LR, #CONSTANT
    where the CONSTANT depends on the specific interrupt (4 for IRQ).

Finally, don't forget to push/pop registers used by this interrupt routine!

*******************************************************************/
// Write code for your IRQ interrupt service routine here
SERVICE_IRQ:
    PUSH {R0-R7, LR} //sparar r0-r7 + lr 
    LDR R4, =0xFFFEC100 //reads the adress of the cpu interface in GIC
    LDR R5, [R4, #0x0C] // read from ICCIAR
    cmp r5, #73
    BEQ PUSH

PUSH:
    LDR r2, =PUSH_BUTTON
	ADD R2, R2, #0xC
    LDR r2, [r2]
	CMP r2, #2
	LDR R1, =CurrentIndex
	LDR R1, [R1]
	LDR R2, =numbers
    ADD R2, R2, R1, LSL #2
	BEQ CHECK_KEY1
CHECK_KEY0:
	ADD R1, R1, #1
	CMP R1, #16
	BNE CHANGE_KEY0
	MOV R1, #0
CHANGE_KEY0:
	LDR R3, =CurrentIndex
	STR R1, [R3]
	LSL R1,R1,#2
	LDR R3, =numbers
	ADD R1,R1,R3
	LDR R1, [R1]
	LDR R2, =SEVEN_DISPLAY
    STR R1, [R2]
	B EXIT_IQR
CHECK_KEY1:
	CMP R1, #0
	SUB R1, R1, #1
	BNE CHANGE_KEY1
	MOV R1, #15
CHANGE_KEY1:
	LDR R3, =CurrentIndex
	STR R1, [R3]
	LSL R1,R1,#2
	LDR R3, =numbers
	ADD R1,R1,R3
	LDR R1, [R1]
	LDR R2, =SEVEN_DISPLAY
    STR R1, [R2]
EXIT_IQR:
	MOV R5, #73
	LDR R4, =0xFFFEC110 //reads the adress of the ICCEOIR
	STR R5, [R4] // write to ICCEOIR
	LDR R4, =0xFF20005C
	MOV R5, #3
	STR R5, [R4]
	POP {R0-R7, LR}
	SUBS PC, LR, #4  // Atomically restores CPSR from SPSR and returns to interrupted instruction.

/****************************************************************************
    Other Interrupt Service Routines (except for IRQ)
    -------------------------------------------------
    
Other interrupts are unused in this program, but should at least be defined.
These interrupt routines can just "idle" if ever called...

****************************************************************************/
// Write code for your other interrupt service routines here
SERVICE_UND:
    B SERVICE_UND
/*--- Software interrupts -----------------------------------------------------*/
SERVICE_SVC:
    B SERVICE_SVC
/*--- Aborted data reads ------------------------------------------------------*/
SERVICE_ABT_DATA:
    B SERVICE_ABT_DATA

/*--- Aborted instruction fetch -----------------------------------------------*/
SERVICE_ABT_INST:
    B SERVICE_ABT_INST
/*--- FIQ ---------------------------------------------------------------------*/
SERVICE_FIQ:
    B SERVICE_FIQ

/*******************************************************************
    HELP FUNCTION!
    --------------

Configures the Generic Interrupt Controller (GIC)
    Arguments:  R0: Interrupt ID

*******************************************************************/
CONFIG_GIC:
    PUSH {LR}
    /* To configure a specific interrupt ID:
    * 1. set the target to cpu0 in the ICDIPTRn register
    * 2. enable the interrupt in the ICDISERn register */
    /* CONFIG_INTERRUPT (int_ID (R0), CPU_target (R1)); */
    MOV R1, #1 // this field is a bit-mask; bit 0 targets cpu0
    BL CONFIG_INTERRUPT
    /* configure the GIC CPU Interface */
    LDR R0, =GIC_CPU_INTERFACE_BASE // base address of CPU Interface, 0xFFFEC100
    /* Set Interrupt Priority Mask Register (ICCPMR) */
    LDR R1, =0xFFFF // enable interrupts of all priorities levels
    STR R1, [R0, #0x04]
    /* Set the enable bit in the CPU Interface Control Register (ICCICR).
    * This allows interrupts to be forwarded to the CPU(s) */
    MOV R1, #1
    STR R1, [R0]
    /* Set the enable bit in the Distributor Control Register (ICDDCR).
    * This enables forwarding of interrupts to the CPU Interface(s) */
    LDR R0, =GIC_DISTRIBUTOR_BASE   // 0xFFFED000
    STR R1, [R0]
    POP {PC}

/*********************************************************************
    HELP FUNCTION!
    --------------

Configure registers in the GIC for an individual Interrupt ID.

We configure only the Interrupt Set Enable Registers (ICDISERn) and
Interrupt Processor Target Registers (ICDIPTRn). The default (reset)
values are used for other registers in the GIC.

Arguments:  R0 = Interrupt ID, N
            R1 = CPU target

*********************************************************************/
CONFIG_INTERRUPT:
PUSH {R4-R5, LR}
/* Configure Interrupt Set-Enable Registers (ICDISERn).
* reg_offset = (integer_div(N / 32) * 4
* value = 1 << (N mod 32) */
LSR R4, R0, #3 // calculate reg_offset
BIC R4, R4, #3 // R4 = reg_offset
LDR R2, =0xFFFED100 // Base address of ICDISERn
ADD R4, R2, R4 // R4 = address of ICDISER
AND R2, R0, #0x1F // N mod 32
MOV R5, #1 // enable
LSL R2, R5, R2 // R2 = value
/* Using the register address in R4 and the value in R2 set the
* correct bit in the GIC register */
LDR R3, [R4] // read current register value
ORR R3, R3, R2 // set the enable bit
STR R3, [R4] // store the new register value
/* Configure Interrupt Processor Targets Register (ICDIPTRn)
* reg_offset = integer_div(N / 4) * 4
* index = N mod 4 */
BIC R4, R0, #3 // R4 = reg_offset
LDR R2, =0xFFFED800 // Base address of ICDIPTRn
ADD R4, R2, R4 // R4 = word address of ICDIPTR
AND R2, R0, #0x3 // N mod 4
ADD R4, R2, R4 // R4 = byte address in ICDIPTR
/* Using register address in R4 and the value in R2 write to
* (only) the appropriate byte */
STRB R1, [R4]
POP {R4-R5, PC}

.end