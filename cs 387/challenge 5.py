# HW5 Challenge Problem 5 

# For this problem, we've attempted to make a
# simplified example demonstrating the beast
# attack.  We've created a simple site
# that has a secret message, `m`.

# You have the ability to send a message, attack, to 
# the server.  The server will prepend
# `attack` to `m` and then encrypt the resulting
# message using CBC mode with a block size
# of 128 bits.  

# The initialization vector, iv, is used from
# the the last block of the last encryption.
# Dave outlined how to deal with and use 
# this in lecture.  He also discussed a paper
# by Thai Duong and Juliano Rizzo that might
# have more useful information

# Specifically, the code below POSTs two values
# `attack` and `token`.  `attack` is the string
# prepended to the message and `token` is used
# internally to maintain a session and keep track
# of the last `iv.`  We highly recommend you don't
# mess with it.
# If `token` is empty or invalid - the server generates a
# random iv value and uses that for the encryption

# Rarely, similar to how a user might close and start
# a new TLS session, the server will start over, pick a new random
# IV and use that for encryption.

# The send function takes in a string as an argument and returns
# a string as an argument.  This is different from previous
# assignments where most functions took in arrays of bits.
# Just remember that each character represents a byte (8 bits)

# More information available: http://forums.udacity.com/cs387-april2012/questions/3506/hw5-5-challenge-question-discussion

###################
# This code is provided as an example of how to send and recieve
# information from the server.
# 
# You should only need to use the `send` function

import urllib
import json
import base64
import copy

BITS = ('0', '1')
ASCII_BITS = 8

def int_to_bits(n):
    return pad_bits(convert_to_bits(n),ASCII_BITS)

def display_bits(b):
    """converts list of {0, 1}* to string"""
    return ''.join([BITS[e] for e in b])

def seq_to_bits(seq):
    return [0 if b == '0' else 1 for b in seq]

def pad_bits(bits, pad):
    """pads seq with leading 0s up to length pad"""
    assert len(bits) <= pad
    return [0] * (pad - len(bits)) + bits

def convert_to_bits(n):
    """converts an integer `n` to bit array"""
    result = []
    if n == 0:
        return [0]
    while n > 0:
        result = [(n % 2)] + result
        n = n / 2
    return result

def string_to_bits(s):
    def chr_to_bit(c):
        return pad_bits(convert_to_bits(ord(c)), ASCII_BITS)
    return [b for group in 
            map(chr_to_bit, s)
            for b in group]

def bits_to_int(b):
    value = 0
    for e in b:
        value = (value * 2) + e
    return value

def bits_to_char(b):
    assert len(b) == ASCII_BITS
    value = bits_to_int(b)
    return chr(value)

def list_to_string(p):
    return ''.join(p)

def bits_to_string(b):
    return ''.join([bits_to_char(b[i:i + ASCII_BITS]) 
                    for i in range(0, len(b), ASCII_BITS)])

def hash(input_, length):
    h = sha512(bits_to_string(input_)).digest()
    return string_to_bits(h)[:length]

def xor(a, b):
    assert len(a) == len(b)
    return [aa^bb for aa, bb in zip(a, b)]

def oaep_pad(message, nonce, g, h):
    mm = message + [0] * (g - len(message))
    G = xor(mm, hash(nonce, g))
    H = xor(nonce, hash(G, h))
    return G + H
    
def encrypt(message, n, public_key, nonce, g, h):
    oaep = oaep_pad(message, nonce, g, h)
    m_int = bits_to_int(oaep)
    return convert_to_bits(pow(m_int, public_key, n))

def decrypt(ciphertext, n, private_key, g, h):
    cipher = string_to_bits(ciphertext)
    c_int = bits_to_int(cipher)
    m_int = pow(c_int, private_key, n)
    m_int = convert_to_bits(m_int)
    oaep = pad_bits(m_int, g+h)
    G = oaep[:g]
    H = oaep[g:]
    nonce = xor(H, hash(G, h))
    mm = xor(G, hash(nonce,g))
    return bits_to_string(mm[:g])


BLOCK_SIZE = 128
site = "http://cs387.udacity-extras.appspot.com/beast"

def unencode_json(txt):
    d = json.loads(txt)
    return dict((str(k),
                 base64.urlsafe_b64decode(str(v)))
                for k,v in d.iteritems())

def _send(attack=None, token=None):
    data = {}
    if attack is not None:
        data["attack"] = base64.urlsafe_b64encode(attack)
    if token is not None:
        data["token"] = base64.urlsafe_b64encode(token)

    # here we make a post request to the server, sending
    # the attack and token data
    json = urllib.urlopen(site, urllib.urlencode(data)).read()
    json = unencode_json(json)
    return json
    
_TOKEN = None
def send(attack=None):
    """send takes a string (representing bytes) as an argument 
    and returns a string (also, representing bytes)"""
    global _TOKEN
    json = _send(attack, _TOKEN)
    _TOKEN = json["token"]
    return json["message"]



# End of example code
##################

##################
# Change secret_message to be the decrypted value
# from the server
secret_message = ""

def make_blocks(b):
    blocks = []
    for i in range(len(b)/BLOCK_SIZE):
        blocks.append(b[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE])
    return blocks

def new_cipher(attack):
    m_string = send(attack)
    m_bits = string_to_bits(m_string)
    blocks = make_blocks(m_bits)
    return blocks

def make_zeros(bytes):
    return [0 for _ in range(bytes*ASCII_BITS)]

def beast():
    size = BLOCK_SIZE/ASCII_BITS
    found = string_to_bits('What hat')
    r = make_zeros(size-1-len(found)/ASCII_BITS)
    blocks = new_cipher(bits_to_string(r))
    IV0 = blocks[-1]
    blocks = new_cipher(bits_to_string(r))
    C01 = blocks[0]
    IV1 = blocks[-1]
    for i in range(256):    
        print i
        Pi = xor(xor(IV0,IV1), (r+found+int_to_bits(i)))
        blocks = new_cipher(bits_to_string(Pi))
        if blocks[0] == C01:
            print 'success', bits_to_string(int_to_bits(i))
            break
        IV1 = blocks[-1]

def beast2():
    size = BLOCK_SIZE/ASCII_BITS
    found = ''
    for i in range(48):
        r = make_zeros(size-1-len(found))
        blocks = new_cipher(bits_to_string(r))
        IV0 = blocks[-1]
        blocks = new_cipher(bits_to_string(r))
        C01 = blocks[0]
        IV1 = blocks[-1]
        for i in range(256):    
            print i
            Pi = xor(xor(IV0,IV1), (r+string_to_bits(found)+int_to_bits(i)))
            blocks = new_cipher(bits_to_string(Pi))
            if blocks[0] == C01:
                found += bits_to_string(int_to_bits(i))
                print 'success', bits_to_string(int_to_bits(i)), found
                break
            IV1 = blocks[-1]
    print found

secret = 'What hath God wrought? -Samuel M'

def beast3():
    size = BLOCK_SIZE/ASCII_BITS
    
    found = 'ught? -Samuel M'
    #found = secret[-15:]
    for i in range(1):
        r = make_zeros(15)
        blocks = new_cipher(bits_to_string(r))
        IV1 = blocks[-1]
        IV0 = blocks[1]
        C01 = blocks[2]
        for i in range(256):    
            print i
            Pi = xor(xor(IV0,IV1), (string_to_bits(found)+int_to_bits(i)))
            blocks = new_cipher(bits_to_string(Pi))
            if blocks[0] == C01:
                found += bits_to_string(int_to_bits(i))
                print 'success', bits_to_string(int_to_bits(i)), found
                break
            IV1 = blocks[-1]
    print found



beast3()


