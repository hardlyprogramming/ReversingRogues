'''
.hardlyprogramming
This code could most definitely be optimized.  I simply followed the assembly for the 
most part and favored readability. I think?
'''
# initialize some variables
C1 = 'A493N36S1QQBTC80'
C2 = [0xc, 0x2c, 0x5c, 0x99, 0x83, 0x5c, 0x9c, 0x11, 0xbc, 0x4d, 0x54, 0x4f, 0x65, 0x35, 0xc6, 0x64]

email = 'abz@def.com'
email = email.upper()

loop1_mem = [0,0,0,0,0,0,0,0]
loop2_mem = [0,0,0,0,0,0,0,0]

sum1 = 0
sum2 = 0
sum_total = 0

sk = []

eax=0
# LOOP 1
for letter in email:
    temp_val = ord(letter) + 0x12
    loop1_mem[eax] = loop1_mem[eax] ^ temp_val
    sum1 += loop1_mem[eax]
    eax += 1
    if eax == 8:
        eax = 0
# LOOP 2
for letter in C1:
    temp_val = ord(letter) + 0x19
    loop2_mem[eax] = loop2_mem[eax] ^ temp_val
    sum2 += loop2_mem[eax]
    eax += 1
    if eax == 8:
        eax = 0
# cumulative sum
sum_total = sum1 + sum2
sum_total = sum_total & -2147483137 #0x800001ff
# check if signed and act accordingly
if sum_total < 0:
    sum_total -= 1
    sum_total |= -512 #0xfffffe00
    sum_total += 1
    #print('sum: ', sum_total)
    
eax = 0
# LOOP 3
while eax < 8:
    loop2_mem[eax] = loop2_mem[eax] ^ C2[eax]
    temp_val = loop2_mem[eax]
    temp_val = temp_val ^ loop1_mem[eax]
    temp_val = temp_val & -2147483137 #0x800001ff
    if temp_val < 0:
        temp_val -= 1
        temp_val |= -512
        temp_val += 1
        
    temp_val = temp_val - sum_total
    
    if temp_val < 0:
        temp_val *= -1  
    if temp_val > 255:
        # shift right 4 bits
        temp_val = temp_val >> 4
        
    eax +=1

    # append hex value as upper without '0x'
    sk.append('{:02X}'.format(temp_val))
    
# i'm lazy
serial = '-'.join([''.join(sk[i:i+2]) for i in range(0, len(sk), 2)])
print(f'Email: {email}')
print(f'Serial: {serial}')
