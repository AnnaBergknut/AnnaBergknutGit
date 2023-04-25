.text
.global _start

_start:
    LDR sp, =#0x10000000
//    LDR sp, =#0x3FFFFFFF-3
    MOV r0, #4
    BL sumOdd   // sumOdd(4)

_halt:
    b _halt

sumOdd:
    PUSH {r4, lr}

    /* Subrutinens funktionella kod */
	CMP 	r0, #0
	BEQ		lBase		// hoppa ur om argumentet är noll
	ADD		r4, r0, r0	// beräkna 2*n (=n+n) till r4 
	SUB 	r4, r4, #1	// beräkna 2*n-1 till r4
	SUB		r0, r0, #1	// minska argumentet med 1
	BL		sumOdd		// anropa funktionen själv - rekursivt
	ADD 	r4, r4, r0  // 2*n-1 + returvärdet
	BAL		lReturn     // ovillkorligt hopp
lBase:
		MOV		r4,#0	// basfall
lReturn:	
		MOV		r0,r4	// flytta returvärde till returregister

    /* Return */
    POP {r4, pc}
//    bx lr

.end