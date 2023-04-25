/**********************************************************************************
* This program demonstrates use of interrupts with assembly code.
*
* It first starts the Altera interval timer (at address 0xFF202000).
*
* The interrupt service routine for the interval timer displays a rotating pattern
* on the LED lights.
*
* It is possible to extend the program to let the user shift rotating direction (left/right).
* This can be done by changing the global variable LEDS_ROTATE_DIR from a switch or
* a pushbutton or by other means.
*
* Note! Some constants, such as adresses to different I/O devices, are hard coded. 
* In these cases there are often also a commented code line with a proposed constant name.
* A better solution should be to define those constant names with .EQU directives:)
*
***********************************************************************************/

/*********************************************************************************
* Initialize the exception vector table
********************************************************************************/
//.section .vectors, "ax"
.org 0x00000000  // Similar to .section above
B _start // reset vector
B SERVICE_UND // undefined instruction vector
B SERVICE_SVC // software interrrupt vector
B SERVICE_ABT_INST // aborted prefetch vector
B SERVICE_ABT_DATA // aborted data vector
.word 0 // unused vector
B SERVICE_IRQ // IRQ interrupt vector
B SERVICE_FIQ // FIQ interrupt vector


.data
/* Global variables */
PATTERN:
    .word 0x0F0F0F0F // pattern to show on the LED lights
LEDS_ROTATE_DIR: // rotating direction
    .word 0


.text

/*
* Reset service routine.
* This is the start of life for the program after reset.
*
* Sets up initial system configuration, such as separate stacks for different
* processor modes. Finally enables the IRQ interrupt, before running
* the main program in SVC mode.
*
* Note! This reset interrupt service routine never "returns from interrupt", 
* because there is nothing to return to. It simply starts the main program.
*/
.global _start
_start:
    /* Set up stack pointers for IRQ and SVC processor modes */
//    MOV R1, #INT_DISABLE | IRQ_MODE
    MOV R1, #0b11010010 // interrupts masked, MODE = IRQ
    MSR CPSR_c, R1 // Change to IRQ mode. CPSR_c means only move the control bits [7:0]
//    LDR SP, =A9_ONCHIP_END - 3  // set IRQ stack to top of A9 onchip memory
    LDR SP, =0xFFFFFFFF - 3 // set IRQ stack to A9 onchip memory


    /* Change to SVC (supervisor) mode with interrupts disabled */
//    MOV R1, #INT_DISABLE | SVC_MODE
    MOV R1, #0b11010011 // interrupts masked, MODE = SVC
    MSR CPSR_c, R1 // change to supervisor mode
//    LDR SP, =DDR_END - 3 // set SVC stack to top of DDR3 memory
    LDR SP, =0x3FFFFFFF - 3 // set SVC stack to top of DDR3 memory

    BL CONFIG_GIC   // configure the ARM generic interrupt controller

    BL CONFIG_INTERVAL_TIMER // configure the Altera interval timer

    /* enable IRQ interrupts in the processor */
//    MOV R1, #INT_ENABLE | SVC_MODE // IRQ unmasked, MODE = SVC
    MOV R1, #0b01010011 // IRQ unmasked, MODE = SVC
    MSR CPSR_c, R1

/*
* Main program now only waits for events/interrupts to handle!
*/
LOOP:
    B LOOP


/*
* Configure the Altera interval timer to create interrupts at 50-msec intervals
*/
CONFIG_INTERVAL_TIMER:
//    LDR R0, =TIMER_BASE
    LDR R0, =0xFF202000
    /* set the interval timer period for scrolling the LED displays */
    LDR R1, =5000000 // 1/(100 MHz) x 5x10^6 = 50 msec
    STR R1, [R0, #0x8]  // store the low half word of counter
                        // start value
    LSR R1, R1, #16
    STR R1, [R0, #0xC]  // high half word of counter start value
                        // start the interval timer, enable its interrupts
    MOV R1, #0x7 // START = 1, CONT = 1, ITO = 1
    STR R1, [R0, #0x4]
    BX LR


/*
* Configure the Generic Interrupt Controller (GIC)
*/
CONFIG_GIC:
    /* configure the HPS timer interrupt */
    LDR R0, =0xFFFED8C4 // ICDIPTRn: processor targets register
    LDR R1, =0x01000000 // set target to cpu0
    STR R1, [R0]

    LDR R0, =0xFFFED118 // ICDISERn: set enable register
    LDR R1, =0x00000080 // set interrupt enable
    STR R1, [R0]
    
    /* configure the FPGA IRQ0 (interval timer) and IRQ1 (KEYs) interrupts */
    LDR R0, =0xFFFED848 // ICDIPTRn: processor targets register
    LDR R1, =0x00000101 // set targets to cpu0
    STR R1, [R0]
    
    LDR R0, =0xFFFED108 // ICDISERn: set enable register
    LDR R1, =0x00000300 // set interrupt enable
    STR R1, [R0]
    
    /* configure the GIC CPU interface */
//    LDR R0, =MPCORE_GIC_CPUIF // base address of CPU interface
    LDR R0, =0xFFFEC100 // base address of CPU interface
   
    /* Set Interrupt Priority Mask Register (ICCPMR) */
    LDR R1, =0xFFFF // 0xFFFF enables interrupts of all
                    // priorities levels
//    STR R1, [R0, #ICCPMR]
    STR R1, [R0, #0x04]
   
    /* Set the enable bit in the CPU Interface Control Register (ICCICR). This bit
    * allows interrupts to be forwarded to the CPU(s) */
//    MOV R1, #ENABLE
    MOV R1, #1
//    STR R1, [R0, #ICCICR]
    STR R1, [R0]
   
    /* Set the enable bit in the Distributor Control Register (ICDDCR). This bit
    * allows the distributor to forward interrupts to the CPU interface(s) */
//    LDR R0, =MPCORE_GIC_DIST
    LDR R0, =0xFFFED000
//    STR R1, [R0, #ICDDCR]
    STR R1, [R0]
    BX LR

/*
* Basic Interrupt Service Routines (ISR) for different interrupt types (except reset).
*
* IRQ is the only interrupt handled by this program (except reset).
* Other interrupts will be ignored here.
*/

/*--- IRQ ---------------------------------------------------------------------
* This is the IRQ Interrupt Service Routine.
*
* Handles interrupts from the Interval Timer, via the Generic Interrupt Controller (GIC).
* 
*/
SERVICE_IRQ:
    PUSH {R0-R7, LR}

    /* Read the Interrupt Acknowledge Register (ICCIAR) from the CPU interface */
 //   LDR R4, =MPCORE_GIC_CPUIF
    LDR R4, =0xFFFEC100
 //   LDR R5, [R4, #ICCIAR] // read the interrupt ID
    LDR R5, [R4, #0x0C] // read from ICCIAR

INTERVAL_TIMER_CHECK:
//    CMP R5, #INTERVAL_TIMER_IRQ // check for interval timer interrupt
    CMP R5, #72 // check for interval timer interrupt
    BNE UNEXPECTED
    BL TIMER_ISR
    B EXIT_IRQ

UNEXPECTED:
    B UNEXPECTED // if not recognized, stop here

EXIT_IRQ:
    /* Write to the End of Interrupt Register (ICCEOIR) */
//    STR R5, [R4, #ICCEOIR]
    STR R5, [R4, #0x10] // write to ICCEOIR

    // Restore registers and return from interrupt.
    POP {R0-R7, LR}
    SUBS PC, LR, #4  // Atomically restores CPSR from SPSR and returns to interrupted instruction.


/*--- Undefined instructions --------------------------------------------------*/
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



/*****************************************************************************
* Interval timer interrupt service routine
*
* Shifts a PATTERN being displayed on the LED lights. The shift direction
* is determined by the external variable LEDS_ROTATE_DIR.
*
******************************************************************************/
TIMER_ISR:
    PUSH {R4-R7}
//    LDR R1, =TIMER_BASE // interval timer base address
    LDR R1, =0xFF202000 // interval timer base address
    MOVS R0, #0
    STR R0, [R1] // clear the interrupt

//    LDR R1, =LED_BASE // LED base address
    LDR R1, =0xFF200000 // LED base address
    LDR R2, =PATTERN // set up a pointer to the pattern for LED displays
    LDR R7, =LEDS_ROTATE_DIR // set up a pointer to the shift direction variable

    LDR R6, [R2] // load pattern for LED displays
    STR R6, [R1] // store to LEDs

SHIFT:
    LDR R5, [R7] // get shift direction
//    CMP R5, #RIGHT
    CMP R5, #1
    BNE SHIFT_L
    MOVS R5, #1 // used to rotate right by 1 position
    RORS R6, R5 // rotate right
    B END_TIMER_ISR
SHIFT_L:
    MOVS R5, #31 // used to rotate left by 1 position
    RORS R6, R5
END_TIMER_ISR:
    STR R6, [R2] // store LED display pattern
    POP {R4-R7}
    BX LR


.end
