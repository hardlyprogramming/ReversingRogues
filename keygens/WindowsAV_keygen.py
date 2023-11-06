import random

# useable letters and numbers (No 'F, C, A, E')
chars = 'BDGHIJKLMNOPQRSTUVWXYZ'

# useable numbers for the last character of serial
nums = '123'

# Serial Format:  *F** - ***C - **A* - E**1

x = '*F**-***C-**A*-E**$'
serial = ''

for char in x:
    if char == '*':
        char = random.choice(chars)
    if char  == '$':
        char = random.choice(nums)
    serial += char
    
print(serial)
