.global main # startpunkt som länkaren känner igen
.text # deklaration av text-sektion (kodavsnitt)
main:
    pushq $0 #för stack alignment 16 bytes
    movq $message, %rdi
    call printf
    call exit
.data # deklaration av data-sektion
    message: .asciz "Hello world!\n" # definition av sträng