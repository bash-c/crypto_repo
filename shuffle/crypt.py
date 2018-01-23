import random
import string

characters = ''.join(map(chr, range(0x20, 0x7f)))

with open('plain.txt', 'r') as fin:
    plaintext = fin.read()

mapping = list(characters)
random.shuffle(mapping)
mapping = ''.join(mapping)

T = str.maketrans(characters, mapping)

with open('crypted.txt', 'w') as fout:
    fout.write(plaintext.translate(T))

plain = list(plaintext)
random.shuffle(plain)
suffled_plaintext = ''.join(plain)

with open('plain.txt', 'w') as frandom:
    frandom.write(suffled_plaintext)
