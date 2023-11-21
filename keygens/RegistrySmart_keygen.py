'''
.hardlyprogramming

Nearly an identicle clone of AdwareAlert serial creation process.  Some minor changes were necessary.

'''
# initialize some variables
C1 = 'A495GR4G67655RTC80' #'A493N36S1QQBTC80'
C2 = [0x0, 0xc, 0x2c, 0x5c, 0x99, 0x83, 0x5c, 0x9c, 0x11, 0xbc, 0x4d, 0x54, 0x4f, 0x65, 0x35, 0xc6, 0x64]

email = input('Enter Email Address: ')
email = email.upper()
email = email + '__UNLIMITED__'

loop1_mem = [0,0,0,0,0,0,0,0,0]
loop2_mem = [0,0,0,0,0,0,0,0,0]

sum1 = 0
sum2 = 0
sum_total = 0

sk = []

eax=1
# LOOP 1
for letter in email:
    temp_val = ord(letter) + 0x12
    loop1_mem[eax] = loop1_mem[eax] ^ temp_val
    sum1 += loop1_mem[eax]
    eax += 1
    if eax == 9:
        eax = 1
# LOOP 2
for letter in C1:
    temp_val = ord(letter) + 0x19
    loop2_mem[eax] = loop2_mem[eax] ^ temp_val
    sum2 += loop2_mem[eax]
    eax += 1
    if eax == 9:
        eax = 1
# cumulative sum
sum_total = sum1 + sum2
sum_total = sum_total & -2147483137 #0x800001ff
# check if signed and act accordingly
if sum_total < 0:
    sum_total -= 1
    sum_total |= -512 #0xfffffe00
    sum_total += 1

eax = 1
# LOOP 3
while eax < 9:
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
email = email.removesuffix('__UNLIMITED__')
print(f'Email: {email}')
print(f'Serial: {serial}')

