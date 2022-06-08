import hashlib
zero = 1810713396
hashed_seed = hashlib.sha1(
    zero.to_bytes(8, byteorder='big')).hexdigest()
print(hashed_seed)