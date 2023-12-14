import random


def gen_chars():
    return(random.randint(0x1000,0xffff))
    

def math1(chars, table_val, remainder):
    esi = chars * 0x100215
    ecx = table_val
    esi = esi + ecx
    ecx = esi
    ecx = ecx & 0x56b64a
    ecx = ecx << 7
    esi = esi ^ ecx
    esi = esi & 0x00000000ffffffff # mask?

    edx = esi
    edx = edx & 0xffffb716
    eax = remainder #  not sure
    edx = edx << 0xf
    esi = esi ^ edx
    esi = esi & 0x00000000ffffffff
    eax = esi
    eax = eax >> 0x10
    eax = eax ^ esi
    eax = eax ^ 0x100215
    eax = eax & 0x00000000ffffffff
    
    return(eax)
    
    
    
def create_serial(chars1, chars2, chars3, chars4, chars5):
    chars1 = format(chars1, '04x')
    chars2 = format(chars2, '04x')
    chars3 = format(chars3, '08x')
    chars4 = format(chars4, '08x')
    chars5 = format(chars5, '08x')
    
    serial = (f'{chars1}-',
    f'{chars2}-',
    f'{chars3[0:4]}-',
    f'{chars3[4:]}-',
    f'{chars4[0:4]}-',
    f'{chars4[4:]}-',
    f'{chars5[0:4]}-',
    f'{chars5[4:]}')

    return(''.join(serial))
    
def get_hex_value_by_number(number):
    # Dictionary containing remainders and their corresponding hex values with keys in ascending order
    hex_values = {
        0: '95F24DAB',
        1: 'B657F9DD',
        2: 'E76CCAE7',
        3: 'AF3EC239',
        4: '715FAD23',
        5: '24A590AD',
        6: '69E4B5EF',
        7: 'BF456141',
        8: '96BC1B7B',
        9: 'A7BDF825',
        10: 'C1DE75B7',
        11: '8858A9C9',
        12: '2DA87693',
        13: 'B657F9DD',  # Corresponding to remainder 1 and 13
        14: 'FFDC8A9F',
        15: '8121DA71',
        16: '8B823ECB',
        17: '885D05F5',
        18: '4E20CD47',
        19: '5A9AD5D9',
        20: '512C0C03',
        21: 'EA857CCD',
        22: '4CC1D30F',
        23: '8891A8A1',
        24: 'A6B7AADB'
    }

    # Check if the number exists in the dictionary keys
    if number in hex_values:
        return int(hex_values[number],16)  # Return corresponding hex value
    else:
        return None  # Return None if number doesn't match any remainder

chars1 = gen_chars()
chars2 = gen_chars()

remainder = chars1 % 25
table_val = get_hex_value_by_number(remainder)
chars3 = math1(chars1, table_val, remainder)

remainder = chars2 % 25
table_val = get_hex_value_by_number(remainder)
chars4 = math1(chars2, table_val, remainder)

remainder = chars4 % 25
table_val = get_hex_value_by_number(remainder)
chars5 = math1(chars4, table_val, remainder)

serial = create_serial(chars1, chars2, chars3, chars4, chars5)

print('Serial: ', serial)
