import random
import string

raw = '***7-***C-***D-***3'

serial = ''.join(random.choice(string.ascii_uppercase+string.digits) if char == '*' else char for char in raw)

print(serial)
