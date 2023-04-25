    .data	
numbers: 
	.word	2, 5, 8, 3, 9, 12, 0	// numbers[0]=2, numbers[1]=5, etc (tabell)
sum:	
	.space	 4					// sum är fyra byte stor (word)
	
	.text        
    .global main
//	.global _start				// CPUlator default
/*  This is a comment */
// This is also a comment
//_start
main:
    LDR     r1, =numbers		// r1 <- basadressen till tabellen, pekar på numbers[0]
    MOV		r0, #0				// r0 <- talet 0 (Vi nollställer summan)
	MOV r3, #0					// r3 = index i tabellen
again:	
//	LDR		r2,[r1]				// r2 <- numbers[i]
	LDR		r2,[r1, r3, LSL #2]	// r2 <- numbers[i], som ligger på basadress + (index * 4)
	CMP		r2, #0				// jämför r2 och 0 (dvs numbers[i]=0?)
	BEQ		finish				// Om lika gå till finish. (dvs vi avslutar vid nolla)
	ADD		r0, r0, r2			// r0 ökas med numbers[i] (dvs summera)
//	ADD		r1, r1, #4			// r1 ökas med 4 (Stega fram ett word = 4 bytes)
	ADD r3, r3, #1				// index++
	B		again				//		(nu pekar r1 på nästa numbers[i]) 
finish:	
	LDR		r1, =sum			// r1 <- basadressen till sum
	STR		r0, [r1]			// r0 -> sum
halt:
	BAL		halt				// Branch Always (hoppa alltid, dvs oändlig loop)
    
	.end
