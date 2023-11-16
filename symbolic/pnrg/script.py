from pwn import *
import time
import subprocess
from functools import reduce
import z3
import random

def hex2int(data, byteorder="little"):
	if isinstance(data, str):
		return int(data, 16)
	elif isinstance(data, bytes):
		return int.from_bytes(data, byteorder="little")
	else:
		raise TypeError("hex2int: datum provided is neither str, or bytes object")

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
def getlong(r):
	return hex2int(r.recvuntilS(b",")[2:-1])

# I cant reassign list in parameter and reflect edit outside function
# I am forced to return the new list
def pnrg_init(seed):
	pnrg_temp = [0] * 1248

	m_pnrg_init(pnrg_temp, seed)
	return pnrg_temp

def m_pnrg_init(pnrg, seed):
	pnrg[1247] = 1
	pnrg[0] = seed
	while(True):
		counter = pnrg[1247]
		if counter > 0x26f:
			break
		pnrg[counter] = 6069 * pnrg[counter-1]
		pnrg[1247] += 1
	return counter

def getRandLong(pnrg):
	mag_3808 = [0, 0x9908B0DF]
	if pnrg[0] >= 624:
		if pnrg[0] >= 625:
			m_pnrg_init(pnrg, 0x1105)
		for i in range(227):
			v4 = pnrg[i] & 0x80000000 | pnrg[2 * i] & 0x7FFFFFF
			pnrg[i] = mag_3808[v4 & 1] ^ (v4 >> 1) ^ pnrg[2 * i + 792]
		while i <= 622:
			v5 = pnrg[i] & 0x80000000 | pnrg[2 * i] & 0x7FFFFFFF
			pnrg[i] = mag_3808[v5 & 1] ^ (v5 >> 1) ^ pnrg[i - 227]
			i += i
		v6 = pnrg[1245] & 0x80000000 | pnrg[0] & 0x7FFFFFFF
		pnrg[1245] = mag_3808[v6 & 1] ^ (v6 >> 1) ^ pnrg[791]
		pnrg[0] = 0
	counter = pnrg[0]
	pnrg[0] = counter + 1
	v7 = pnrg[counter] >> 11 ^ pnrg[counter]
	v8 = (((v7 << 7) & 0x9D2C5680 ^ v7) << 15) & 0xEFC60000 ^ (v7 << 7) & 0x9D2C5680 ^ v7
	return (v8 >> 18) ^ v8

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

#LIBC = ELF("./path")
#LIBC.address = 0xbase
#LIBC.symbols["__symol_name"]

time.sleep(0.5)
long = getlong(r)
seed = z3.BitVec("seed", 32)


pnrg=pnrg_init(seed)
for i in range(1000):
	getRandLong(pnrg)
result = getRandLong(pnrg)

solver = z3.Solver()
solver.add(seed = result)
print(solver.check())
model = solver.model()
print(model.eval(seed))

r.interactive()
