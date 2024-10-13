# ODC_23-24-CTFs <!-- omit in toc -->

> POLIMI Offensive and Defensive Cybersecurity (ODC) 23/24 course's CTFs solved

- [1. About](#1-about)
  - [1.1. What is a CTF?](#11-what-is-a-ctf)
  - [1.2. What is a "flag"?](#12-what-is-a-flag)
  - [1.3. What are the macro-topics?](#13-what-are-the-macro-topics)
  - [1.4. 23/24 ODC CTFs](#14-2324-odc-ctfs)
- [2. File structure and convetions](#2-file-structure-and-convetions)
- [3. Usage](#3-usage)
- [4. Contibutions](#4-contibutions)
  - [4.1. Enhancement](#41-enhancement)
  - [4.2. New exploit](#42-new-exploit)
- [5. Meta](#5-meta)

# 1. About

## 1.1. What is a CTF?
Capture The Flag (CTF) is a cybersecurity challenge that involves participants finding a designated flag. The flag is acquired when a participant successfully gains control of the organizer's publicly vulnerable machine. Typically, CTFs are organized into macro-topics within a jeopardy-style competition, allowing individuals or teams to participate through the central organizer's online platform. Additionally, other cybersecurity competitions, such as "Attack/Defense" or "King of the Hill," also exist.

## 1.2. What is a "flag"?
A flag typically consists of a unique and non-trivial string of characters and symbols stored in a file named "flag". This file is configured to be readable exclusively by the organizers, accessible only through the "root" account (also known as "superuser" or "admin") on the machine. The term "taking control" refers to the successful attainment of root privileges on the machine. Reading the flag and subsequently reporting it to the organizers serves as a harmless proof of accomplishment.

## 1.3. What are the macro-topics?
Competitions may encompass one or more macro-topics, which can include areas such as cryptography, reverse engineering, binary exploitation, web application security, steganography/forensics, mobile security, and other related domains.

## 1.4. 23/24 ODC CTFs
POLITECNICO DI MILANO (POLIMI) offers an advanced technical course on Cybersecurity: "Offensive and Defensive Cybersecurity". 
All along the course, students are being presented with CTFs comprising these topics in macro-topics:
 - shellcode (binary exploitation)
 - reversing (reverse engineering)
 - mitigations (mitigations bypass, binary exploitation)
 - ROP (Return Oriented Programming, binary exploitation)
 - HEAP (HEAP exploitation, binary exploitation)
 - symbolic (symbolic execution, binary exploitation)
 - race (race conditions, web app exploitation)
 - serialization (serialization, web app exploitation)
 - XSS (cross-site scripting, web exploitation)
 - malware (packing, binary analysis)

to solve by applying what has been learned in class.
Final exam consists in an actual free-for-all live CTF competition of 7 hours long.

# 2. File structure and convetions
CTFs are organized in subdirectories, grouped inside parent directories reflecting each topic. 

Inside each CTF directory, you can usually find (depending on the macro-topic):
 - `notes.txt`: a text file within all my notes taken live.
 - The executable file: the binary to be exploited. It has no file extension. Usually, source code is not given.
 - `*.mod`: modified versions of the executable
 - `script.py`: the Python exploiting script. The main entry point file of every CTF directory. Usually, you should run it once and get  to output the flag.
 - `payload`: optional file with malicious content. It is used by `script.py`. 
 - `libc*.so` and `ld*.so`: sometimes, it is also given the standard C library and loader, supposed to run with the executable.
 - `src/` or `html` or `htdocs`: folder containing the source code. Usually given for web app exploitation.
 - `explanation.md`: text markdown file in which it is clearly detailed the exploit in steps.
 - An optional child directory named after a *contributor* with a different exploit inside.

# 3. Usage
Challenges are hosted at [https://training.offdef.it/challenges](https://training.offdef.it/challenges) under form of provided services.

**NOTE**: Before running any file, check if the service is up by sending a TCP request: `nc -zv {hostname} {port}`. 

`script.py` should interact with the service, exploit it and printing the flag. You can consult documentation on the CTF by reading the `explanation.md` file.

# 4. Contibutions
Contributions are more than welcome! Here's a [short video tutorial](https://www.youtube.com/watch?v=8lGpZkjnkt4) on how to open a *pull request*.

## 4.1. Enhancement
If you just thought something could have been done better or you want to fix a mistake, In the pull request, write a brief description of what you *enhanced*.

## 4.2. New exploit
If you want to submit a new exploit, follow these steps:
1. Create a subdirectory with your name in your desired specific CTF folder: `foo/CTF$: mkdir {name}`
2. Inside that directory, there should be at least:
   - One `script.py` file with your exploit inside it.
   - One `explanation.txt` with a clear and concise explanation in steps of your exploit.
   - You can add any other file you think will be useful.
3. State in the pull request message that it is a "New exploit" contribution.

# 5. Meta
gcsar

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/thisisnotgcsar/ODC_23-24-CTFs">ODC_23_24</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/thisisnotgcsar">gcsar</a> is licensed under <a href="http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-NC-SA 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1"></a></p>

https://github.com/thisisnotgcsar
