.text
.global _start

_start:
    LDR sp, =#0x10000000
//    LDR sp, =#0x3FFFFFFF-3
    MOV r0, #0
    BL komplex

_halt:
    b _halt

komplex:
	PUSH {r4, lr}	 	/* Prolog */
	MOV	 r4, r0
	ADD  r4, r4, #4		/* öka med 4 */
	MOV  r0, r4
	BL   increment		/* hoppa till subrutinen */
	ADD	 r4, r0, #4		/* öka med 4 igen */
	MOV  r0, r4
	POP  {r4, pc}		/* Epilog */

/* Anropar inga subrutiner */
/* Om bara register r12 används behöver vi inte använda stacken */
/* Indata r0 */
/* Utdata r0 */
increment:	/* label, gör att vi kan använda namnet som adress */
	ADD r12, r0, #1		/* addera argumentet med 1 */
	MOV r0, r12		    /* lägg över i r0 */
	BX 	lr			    /* återhopp */


.end