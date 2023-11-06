import hashlib

email = str(input('Enter email: ')) # get email from user
email += 'edinichka' # append 'edinichka''

m = hashlib.md5(email.encode('utf-8')).hexdigest() # md5 hash
m = m[6:22].upper() # take chars from index 6 to 21

print(f'Serial: {m}')
