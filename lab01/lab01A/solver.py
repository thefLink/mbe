# username: kkkkkk
# password: 6232823
# 1uCKy_Gue55

username = 'kkkkkk'
superserial = (ord('k')^0x1337)+6221293
for i in range(0,len(username)):
  superserial+=(superserial ^ ord(username[i]))%0x539

print superserial
