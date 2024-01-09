import z3
from pwn import *

# function used to read the 1000th random generated number
def getlong(r):
	return int(r.recvuntilS(b",")[2:-1], 16)

# function from the program
# probably its an initialization function of the prng data structure
# data structure is an array in which:
#   - first element is the seed
#   - last element is a counter
#   - in between all numbers
def m_seedRand(pnrg, seed):
	pnrg[0] = seed # seed
	pnrg[624] = 1 # counter
	while(True):
		index = pnrg[624]
		if index > 623:
			break
		pnrg[pnrg[624]] = 6069 * pnrg[pnrg[624] - 1] # initialize the element of the array similar as an cbc mode
		pnrg[624] += 1 # increment counter

# utility function used by the program
def mag(val):
    return z3.If(val == 0, z3.BitVecVal(0x0, 32), z3.BitVecVal(0x9908b0df, 32))

# the generator
# this is a porting of the original function
def genRandLong(pnrg):
	if pnrg[624] >= 0x270:
		if pnrg[624] >= 0x271:
			m_seedRand(pnrg, 4357)
		for i in range(227):
			v4 = pnrg[i] & 0x80000000 | pnrg[i + 1] & 0x7FFFFFFF
			pnrg[i] = (mag(v4 & 1) ^ z3.LShR(v4, 1) ^ pnrg[i + 397]) & 0xffffffff
		while i <= 622:
			v5 = pnrg[i] & 0x80000000 | pnrg[i + 1] & 0x7FFFFFFF
			pnrg[i] = (mag(v5 & 1) ^ z3.LShR(v5, 1) ^ pnrg[i - 227]) & 0xffffffff
			i += 1
		v6 = pnrg[623] & 0x80000000 | pnrg[0] & 0x7FFFFFFF
		pnrg[623] = (mag(v6 & 1) ^ z3.LShR(v6, 1) ^ pnrg[396]) & 0xffffffff
		pnrg[624] = 0
	v1 = pnrg[624]
	pnrg[624] = v1 + 1
	v7 = z3.LShR(pnrg[v1], 11) ^ pnrg[v1]
	v8 = (((v7 << 7) & 0x9D2C5680 ^ v7) << 15) & 0xEFC60000 ^ (v7 << 7) & 0x9D2C5680 ^ v7
	return (z3.LShR(v8, 18) ^ v8) & 0xffffffff

r = remote("bin.training.jinblack.it", 2020)
time.sleep(0.5)
#r = process("./pnrg")
# we read the seed
long = getlong(r)
print(long)

# the seed is 32 bits, 4 bytes, 1 long
seed = z3.BitVec("seed", 32)
pnrg = [0] * 625

# data structure init
m_seedRand(pnrg, seed)

# we simulate the program
for i in range (1000):
	genRandLong(pnrg)
result = genRandLong(pnrg)

# we add the constraint that our symbolic variable must be equal to the original seed
solver = z3.Solver()
solver.add(result == long)

# find the solution and send it
print(solver.check())
model = solver.model()
number = model.eval(seed)
print("seed:", number)
r.send(str(number).encode())

r.interactive()
