from pwn import *

r = remote("bin.training.offdef.it", 2021)
r.recvuntil(b"continue:")
# this would be the key if there was the condition in angr of only printable chars
#r.send(int("34920187112902781278311238100717355388774617574960413476778239561435950620704").to_bytes(32, "big"))
r.send(int("34919972323007683893813710804696905955157506169022087862543796132380755886080").to_bytes(32, "big"))
r.interactive()
