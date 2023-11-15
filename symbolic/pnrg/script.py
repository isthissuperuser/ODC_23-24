from pwn import *
import time
import subprocess
from functools import reduce

def bytes2int(data, byteordered="little"):
	return int.from_bytes(data, byteordered="little")

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
def take_long(r):
	return int(r.recvuntilS(b",")[:-1], 16)

context.terminal = ['tmux', 'splitw', '-h']
#context.log_level = "warn"
logging.getLogger('pwnlib.elf').setLevel(logging.ERROR)

# breakpoints
b_main = 0xffff

one_gadget=0x00
if args["ONE_GADGET"]:
	one_gadget = int(args["ONE_GADGET"], 16)
if args["REMOTE"]:
	r = remote("bin.training.jinblack.it", 2020)
elif args["GDB"]:
	r = gdb.attach("./pnrg", f"""
		# b *{b_main}
		unset env
		set disable-randomization off
		set debuginfod enabled on
		c
		""")
else:
	r = process("./pnrg")

time.sleep(0.5)
long = take_long(r)
print(long)

r.interactive()
