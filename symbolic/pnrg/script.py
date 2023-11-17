import z3
from pwn import *

def getlong(r):
	return int(r.recvuntilS(b",")[2:-1], 16)
	
def m_seedRand(pnrg, seed):
	pnrg[0] = seed
	pnrg[624] = 1
	while(True):
		index = pnrg[624]
		if index > 623:
			break
		pnrg[pnrg[624]] = 6069 * pnrg[pnrg[624] - 1]
		pnrg[624] += 1

def mag(val):
    return z3.If(val == 0, z3.BitVecVal(0x0, 32), z3.BitVecVal(0x9908b0df, 32))

def genRandLong(pnrg):
	if pnrg[624] >= 0x270:
		if pnrg[624] >= 0x271:
			m_seedRand(pnrg, 4357)
		for i in range(227):
			v4 = pnrg[i] & 0x80000000 | pnrg[i + 1] & 0x7FFFFFFF
			pnrg[i] = mag(v4 & 1) ^ z3.LShR(v4, 1) ^ pnrg[i + 397]
		while i <= 622:
			v5 = pnrg[i] & 0x80000000 | pnrg[i + 1] & 0x7FFFFFFF
			pnrg[i] = mag(v5 & 1) ^ z3.LShR(v5, 1) ^ pnrg[i - 227]
			i += 1
		v6 = pnrg[623] & 0x80000000 | pnrg[0] & 0x7FFFFFFF
		pnrg[623] = mag(v6 & 1) ^ z3.LShR(v6, 1) ^ pnrg[396]
		pnrg[624] = 0
	v1 = pnrg[624]
	pnrg[624] = v1 + 1
	v7 = z3.LShR(pnrg[v1], 11) ^ pnrg[v1]
	v8 = (((v7 << 7) & 0x9D2C5680 ^ v7) << 15) & 0xEFC60000 ^ (v7 << 7) & 0x9D2C5680 ^ v7
	return z3.LShR(v8, 18) ^ v8

r = remote("bin.training.jinblack.it", 2020)
long = getlong(r)

seed = z3.BitVec("seed", 32)
pnrg = [0] * 625

m_seedRand(pnrg, seed)

for i in range (1000):
	genRandLong(pnrg)
result = genRandLong(pnrg)

solver = z3.Solver()
solver.add(result == long)

print(solver.check())
model = solver.model()
number = model.eval(seed)
print("seed:", number)

r.send(str(number).encode())

r.interactive()
