import random
import math


def get_chunk1():
    while True:
        chunk = ''.join(random.choice('abcdef') for _ in range(8))
        if int(chunk,16) % 0x154 == 0:
            return(chunk)
     

def get_chunk2():
    while True:
        chunk = ''.join(random.choice('0123456789') for _ in range(8))
        if int(chunk[0],16) < 8:
            if int(chunk,16) % 0x154 == 0:
                return(chunk)


def get_overflow(num):
    a = hex(num)[2:]
    lower = a[-1:-9:-1][::-1]
    upper = a[-9::-1][::-1]
    if len(upper)<8:
        upper = '0'*(8-len(upper))+upper


    if len(upper) < 8:
        upper = '0'*(8-len(upper)) + upper
    if len(lower) < 8:
        lower = lower + '0'*(8-len(lower))                
    return((upper,lower))


def swap_bytes(frm_reg, to_reg, frm='l', to='x'):
    if frm=='l':
        f = frm_reg[6:]
        if to=='x':
            t = to_reg[0:4] + '00' + f
    elif frm=='h':
        f = frm_reg[4:6]
        if to=='x':
            t = to_reg[0:4] + '00' + f
    elif frm=='ul':
        f = frm_reg[2:4]
        if to=='x':
            t = to_reg[0:4] + '00' + f
    elif frm=='uh':
        f = frm_reg[0:2]
        if to=='x':
            t = to_reg[0:4] + '00' + f
    elif frm =='x':
        f = frm_reg[4:]
        if to=='reg':
            t = '0000' + f
    
    return(t)


def add_reg(reg1, reg2):
    reg1 = hex(int(reg1,16) + int(reg2,16))[2:]
    if len(reg1) > 8:
        reg1 = reg1[1:]
    elif len(reg1) < 8:
        reg1 = '0'*(8-len(reg1))+reg1
    return(reg1)

found = False
while found == False:
    n=0
    test_serials = []
    print('Generating Possibilities...')
    while n<2000:
        chunk2 = get_chunk2()
        chunk1 = get_chunk1()

        final = chunk1+chunk2
        test_serials.append(final)
        n+=1
    print('Finding Serial...')
        
    c1 = []
    c2 = []

    for test_serial in test_serials:
        c1.append(test_serial[0:8])
        c2.append(test_serial[8:])
    for chunk1 in c1:
        if found == False:
            for chunk2 in c2:
         
                serial = f'{chunk1[0:4]}-{chunk1[4:]}-{chunk2[0:4]}-{chunk2[4:]}'
                # ---Check 2---
            
                EDX, EAX = get_overflow(int(chunk1,16) * int(chunk2,16))
                EBX = int(EAX,16)
                EDX, EAX = get_overflow(int(chunk1,16) * int(chunk2,16))

               
                EBX = EBX + int(EAX,16)
               
                EDX, EAX = get_overflow((int(chunk2,16) * int(chunk2,16)))
              
                EDX = int(EDX,16) + EBX

                EDX = hex(EDX)[2:]
                if len(EDX )> 8:
                    EDX = EDX[1:]



                # --- Check 3 --- #
                ECX = chunk2
            

                ECX = swap_bytes(EAX,ECX,frm='l',to='x')
                espc = EAX
                EAX = swap_bytes(EAX,EAX,frm='h',to='x')
                esp10=EDX
                EBX = 0xE2
                ECX = hex(int(ECX,16)+int(EAX,16))[2:]
                EAX = swap_bytes(EAX,EAX,frm='ul',to='x')
                ECX = hex(int(ECX,16)+int(EAX,16))[2:]
                EAX = swap_bytes(EAX,EAX,frm='uh',to='x')
                ECX = add_reg(ECX,EAX)
                EAX = swap_bytes(EDX,EAX,frm='l',to='x')
                EDX = swap_bytes(EDX,EDX,frm='h',to='x')
                ECX = add_reg(ECX,EAX)
                EAX = esp10
                EAX = hex(int(EAX,16) >> 0x10)[2:]
                if len(EAX) < 8:
                    EAX = '0'*(8-len(EAX))+EAX
               
                ECX = add_reg(ECX,EDX)
                EDX = swap_bytes(EAX,EDX,frm='l',to='x')
                EAX = swap_bytes(EAX,EAX,frm='h',to='x')
                ECX = add_reg(ECX,EDX)
                ECX = add_reg(ECX,EAX)
                ECX = swap_bytes(ECX,ECX,frm='x',to='reg')
                EAX = ECX
                EDX = hex(int(EAX,16) % 0xe2)[2:]
                EAX = hex(math.trunc(int(EAX,16) / 0xe2))[2:]
                if int(EDX,16) == 0:
           
                    EAX = ECX
                    
                    old_ecx = EAX
                    EAX = 0
                    if int(chunk2[0],16) < 8: # fixed
                        ECX = int(chunk1,16)
                    else:
                        ECX = int(chunk1,16)-1
                        
                    ECX = ECX | EAX
                    ECX = chunk2
                    EAX = EAX*ECX
                   
                    EBX = EAX
                    EAX = old_ecx

                    if int(chunk2[0],16) < 8: #fixed
                        EDX, EAX = get_overflow(int(chunk1,16) * int(EAX,16))
                    else:
                        EDX, EAX = get_overflow((int(chunk1,16)-1) * int(EAX,16))
                
                    EBX = EAX
                   
                    EAX = old_ecx
                    EDX, EAX = get_overflow(int(EAX,16)*int(ECX,16))
                 
                    EDX = int(EBX,16) + int(EDX,16)
                    EDX = hex(EDX)[2:]
                    old_eax = EAX
                    ECX = 0x67
                    EAX = EDX
                    EDX = hex(int(EAX,16) % 0x67)[2:]
                    EAX = hex(math.trunc(int(EAX,16) / 0x67))[2:]

                   
                    if int(EDX,16) == 0:
                      EAX = old_eax
                      EDX = int(EAX,16) % 0x67
                      EAX = math.trunc(int(EAX,16) / 0x67)
                      if EDX == 0:
                        print('FOUND!')
                        serial = f'{chunk1[0:4]}-{chunk1[4:]}-{chunk2[0:4]}-{chunk2[4:]}'
                        print('Serial: ', serial)
                        found = True
                        break
        
