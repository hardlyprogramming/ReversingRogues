import secrets
import random
import math
import time

def gen_random_chunk2():
    random_int = random.randint(0xaaaaaaaa,0xeeeeeeee)
    random_int = random_int + (0x154 - random_int % 0x154)
    return(random_int)

def gen_random_chunk1(chunk2):
    random_int = secrets.randbits(32)
    if chunk2 >= 2147483648:
        random_int = random_int + (0x154 - random_int % 0x154) + 1
    else:
        random_int = random_int + (0x154 - random_int % 0x154)
        
    return(random_int)


def overflow(num):
    eax = (num & 0x00000000ffffffff)
    edx = (num & 0xffffffff00000000) >> 32
    return(eax, edx)


def add(num1, num2):
    s = (num1 + num2) & 0x00000000ffffffff
    return(s)

    

start_t = time.time()

found = False

print('Generating Serial...')
while found == False:
    
    chunk2 = gen_random_chunk2()
    chunk1 = gen_random_chunk1(chunk2)

    dec = False

    if chunk2 >= 2147483648:
        dec = True
        chunk1 = chunk1 - 1


    eax, edx = overflow(chunk1 * chunk2)
    ebx = eax
    eax, edx = overflow(chunk1 * chunk2)

    ebx = add(ebx,eax)

    eax, edx = overflow(chunk2 * chunk2)
    edx = add(edx,ebx)

    # check 3
    ecx = chunk2
    ecx = (eax&0x000000ff) + (ecx&0xffff0000)
    espc = eax
    eax = ((eax&0x0000ff00)>>8) + (eax&0xffff0000)
    esp10 = edx
    ##    print('--- check 3 ---')
    ##    print('eax: ', hex(eax))
    ##    print('ebx: ', hex(ebx))
    ##    print('ecx: ', hex(ecx))
    ##    print('edx: ', hex(edx))

    ebx = 0xe2
    ecx = add(ecx,eax)
    eax = ((eax&0x00ff0000)>>16) + (eax&0xffff0000)
    ecx = add(ecx,eax)
    eax = ((eax&0xff000000)>>24) + (eax&0xffff0000)
    ##    print('--- check 4 ---')
    ##    print('eax: ', hex(eax))
    ##    print('ebx: ', hex(ebx))
    ##    print('ecx: ', hex(ecx))
    ##    print('edx: ', hex(edx))

    ecx = add(ecx,eax)
    eax = (edx&0x000000ff) + (eax&0xffff0000)
    edx = ((edx&0x0000ff00)>>8) + (edx&0xffff0000)
    ecx = add(ecx,eax)
    eax = esp10
    eax = (eax >> 0x10)
    ##    print('--- check 5 ---')
    ##    print('eax: ', hex(eax))
    ##    print('ebx: ', hex(ebx))
    ##    print('ecx: ', hex(ecx))
    ##    print('edx: ', hex(edx))

    ecx = add(ecx,edx)
    edx = (eax&0x000000ff) + (edx&0xffff0000)
    eax = ((eax&0x0000ff00)>>8) + (eax&0xffff0000)
    ecx = add(ecx,edx)
    ecx = add(ecx,eax)
    ecx = ((ecx&0x0000ffff)) + (ecx&0x00000000)
    eax = ecx
##    print('--- check 6 ---')
##    print('eax: ', hex(eax))
##    print('ebx: ', hex(ebx))
##    print('ecx: ', hex(ecx))
##    print('edx: ', hex(edx))

    edx = eax % 0xe2
    #print('eax: ', hex(eax))
    #eax = math.trunc(eax / 0xe2)
    #print('edx: ', hex(edx))
    if edx == 0:
        eax = ecx

        old_ecx = eax
        eax = 0
        ecx = chunk1
        ecx = ecx | eax
        ecx = chunk2
        eax, edx = overflow(eax*ecx)
        ebx = eax
        eax = old_ecx

        eax, edx = overflow(chunk1 * eax)
        ebx = eax
        eax = old_ecx
        eax, edx = overflow(eax * ecx)

        edx = add(ebx,edx)
        old_eax = eax
        ecx = 0x67
        eax = edx
        edx = (eax%0x67)
        #eax = math.trunc(eax/0x67)

        if edx == 0:
            eax = old_eax
            edx = eax % 0x67
            #eax = math.trunc(eax/0x67)

            if edx == 0:
                print('DONE!')
                if dec:
                    chunk1 = chunk1 + 1
                chunk1 = format(chunk1,'08x')
                chunk2 = format(chunk2, '08x')

                serial = f'{chunk1[0:4]}-{chunk1[4:]}-{chunk2[0:4]}-{chunk2[4:]}'
                print(serial)
                found = True
                break

        
end_t = time.time()

exec_t = end_t - start_t

print('time: ', exec_t)
