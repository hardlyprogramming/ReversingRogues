import random

def get_chunk():
    while True:
        chunk = ''.join(random.choice('abcdef0123456789') for _ in range(8))
        if int(chunk,16) % 0x154 == 0:
            return(chunk)

chunk2 = '0000-0000'
chunk1 = get_chunk()

print('Serial: ', f'{chunk1[0:4]}-{chunk1[4:]}-'+ chunk2)
