#pnrg
 - The program is using a cryptographically unsecure pseudo random number generator to generate number strarting from the seed
 - it generates a thousand of numbers and output to us the last one and then ask us for the original seed
 - if we input the correct original seed the program outputs us the flag
 - In order to arrive to the seed we port the prng ops in python, simulating its behavior and made z3 run through it
 - we put the constraint that the result of our symbolic variable must be the same as the the 1000th number and we obtain the original seed
 - we send the original seed and we get the flag
