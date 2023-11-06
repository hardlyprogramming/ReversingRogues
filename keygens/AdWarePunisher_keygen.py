import hashlib

C1 = int(0xeb39fec5)
C2 = int(0x6D)
C3 = int(0x1F)
C4 = '123456789MNBVCXZLKJHGFDSAOPIUYTRE123456789MNBVCXZLKJHGFDSAOPIUYTRE'


def get_email():
    email = input('Email: ')
    if email == None:
        email = ' '
    return(email)

                                                                                                                                            
def create_md5(email):

    m = hashlib.md5(email.encode('utf-16le'))
    md5 = m.hexdigest()
    return(md5)


def split_hex_string(xstr, split=2):
    temp = ([xstr[i:i+split] for i in range(0, len(xstr), split)])
    return(temp)


def change_endian(xlist):
    # swap endian
    # ie: ABCD -> CDAB
    new_list = []
    for xstr in xlist:
        z = int(xstr, 16)
        z = z.to_bytes(4, byteorder='little')
        new_list.append(str(z.hex()))
    return(new_list)


print('\n\n')
email = get_email()
email = format_email(email)

# create md5 hash of email
md5 = create_md5(email)
# split md5 into 4 byte chunks, big endian
md5 = split_hex_string(md5, split=8)
md5 = change_endian(md5)
                 
storage_1 = []
# perform math operation on md5 with C1 and store in storage_1
for word in md5:
    a = C1 ^ int(word,16)
    # format result as uppercase hex value minus the '0x' ie: 0xab -> AB
    storage_1.append('{:02X}'.format(a))

# swap each 4 byte chunk endian ie: EFCDAB89 -> 89ABCDEF
storage_1 = change_endian(storage_1)
# split each 4 byte chunk into 2 byte chunks ie: 89ABCDEF -> 89, AB, CD, EF
storage_1 = [split_hex_string(x,split=2) for x in storage_1]
# combine all bytes into a single list
storage_1 = [int(item,16) for sublist in storage_1 for item in sublist]
# double the list
storage_1 = storage_1 + storage_1
# perform the math operation with C2
storage_1 = [byte ^ (C2+i) for i, byte in enumerate(storage_1)]
# create serial with bytes from storage_1 an C3
serial = [C4[byte & C3] for byte in storage_1]

print('Serial: '+ ''.join(serial))
print('\n\n')
