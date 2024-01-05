import angr
import claripy
from pwn import *

TARGET = 0x8049843

chars = [claripy.BVS(f"c_{i}", size=8) for i in range(33)]
flag = claripy.Concat(*chars)

proj = angr.Project("./john")
initial_state = proj.factory.entry_state(args=["./john", flag])

#constraint the symbolic chars to be printable characters
for char in chars:
	initial_state.solver.add(char >= 0x20)
	initial_state.solver.add(char <= 0x7e)

#inputting the info we know
initial_state.solver.add(chars[0] == 'f')
initial_state.solver.add(chars[1] == 'l')
initial_state.solver.add(chars[2] == 'a')
initial_state.solver.add(chars[3] == 'g')
initial_state.solver.add(chars[4] == '{')
initial_state.solver.add(chars[32] == '}')

simgr = proj.factory.simulation_manager(initial_state)

solution = ""
while len(simgr.active) > 0:
	print(simgr, simgr.active)
	simgr.explore(find=TARGET, n=1, num_find=1)
	if len(simgr.found) > 0:
		print("wow")
		solution = simgr.found[0].solver.eval(flag)
		print(solution)
		proj.terminate_execution()
		break
