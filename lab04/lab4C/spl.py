#!/usr/local/bin/python2

#  Username: %p ..... %p
password = []
out = "0x756200700x74315f370x7334775f0x625f376e0x337455720x7230665f0x623433630x216531"

hex_encoded = [ x for x in out.split("0x")[1:] ]
[  password.append(x.decode("hex")[::-1]) for x in hex_encoded ]

print ''.join(password)[1:]

