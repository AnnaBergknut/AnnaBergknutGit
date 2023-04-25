.text
.global _start

_start:
    MOV r0, #0
    BL increment

_halt:
    b _halt


/* Anropar inga subrutiner */
/* Om bara register r12 används behöver vi inte använda stacken */
/* Indata r0 */
/* Utdata r0 */
increment:	/* label, gör att vi kan använda namnet som adress */
	ADD r12, r0, #1		/* addera argumentet med 1 */
	MOV r0, r12		    /* lägg över i r0 */
	BX 	lr			    /* återhopp */


.end