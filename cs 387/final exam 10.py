# For this problem, Alice and Bob want to communicate
# They have set up two servers to respond to messages
# and you need to transfer the messages between the two.
#
# The protocol goes as follows:
# 1) a. Establish a session with Alice
#    b. Establish a session with Bob
# 2) a. Send Alice's public information to Bob
#    b. Send Bob's public information to Alice
# 3) Relay messages
#
# Step 1 - Establishing a session
# The function `initialize` can be used to establish a session.
# Alice responds to a POST request with the `type` key set to "init".
# She will send back two values: a token which is used to track the 
# session and a public value, g^x.  The token will expire after 20 minutes,
# so you will need to re-initialize a session after that time
#
# Step 2 - Exchanging public information
# Alice now needs Bob's public value.  The function `send_key` can be
# used to send this.  The function makes a POST request.  Alice responds with 
# a successful status.
#
# Step 3 - Relay messages
# Now that Alice and Bob have a shared secret key, they can use that
# to encrypt secret messages.  You will need to relay these messages.
# Use the `recieve_msg` function to get the first message to send from Alice
# Then, take the values recieved from that and send them to Bob, who will
# respond.  Take his response and send it back to Alice.  Repeat.
#
# Errors
# If you try to do something that Alice and Bob don't like, for example sending a message
# without first exchanging public information, they will respond with 
# a 501 status code and more information in the response.
#
# As with the challenge problem of Unit 5, this assignment requires that
# you run code on your own environment.  It will not work if you write
# code in the Udacity IDE and hit RUN or SUBMIT.
#
# You're allowed to use whatever programming language you want.  The 
# code provide below can be used as a reference implementation.
#

from urllib import urlopen, urlencode
import json
from hashlib import sha1
from Crypto.Cipher import AES
from Crypto.Util import Counter

base = "http://cs387.udacity-extras.appspot.com/final"
Alice = base + "/alice"
Bob = base + "/bob"
Alex = base + '/alex'
Betty = base + '/betty'
Eve = base + '/eve'

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

def xor(a, b):
    assert len(a) == len(b)
    return [aa^bb for aa, bb in zip(a, b)]


def check_output(output):
    data = output.read()
    if output.getcode() != 200:
        raise Exception(data)
    data = json.loads(data)
    return data

def get_pg():
    output = urlopen(base)
    data = check_output(output)
    # returns {"p":<large prime>, "g":<generator for p>}
    return data

def initialize(person):
    data = {'type':'init'}
    output = urlopen(person, urlencode(data))
    data = check_output(output)
    # returns a dictionary 
    # {"token":<token_value>, "public": <g^x>}
    return data

def send_key(person, token, public, name):
    """
    person: url of Alice/Bob
    token: token used to track session
    public: the public value of the other party
    name: the name of the other party - "alice", "bob"
    """
    data = {'type':'key',
            'token':token,
            'public':public,
            'name':name}
    output = urlopen(person, urlencode(data))
    data = check_output(output)
    # Should be a response {"status":"success"}
    return data

def recieve_msg(person, token):
    data = {'type':'msg',
            'token':token}
    output = urlopen(person, urlencode(data))
    data = check_output(output)
    # should be a response
    # {"msg":<cipher>, "iv":<initialization vector>}
    return data

def send_msg(person, token, cipher, iv):
    data = {'type':'msg',
            'token':token,
            'message':cipher,
            'iv':iv}
    output = urlopen(person, urlencode(data))
    data = check_output(output)
    # If the person doesn't have
    # a response to the message, the response will
    # just be {"status":"success"}
    # else, the response will be {"status":"sucess", 
    #                             "reply":{"msg":<cipher>,
    #                                      "iv":<initialization vector>}}
    return data

##########################################################
def hash(b):
    return sha1(bits_to_string(b)).digest()


def communicate(person_a, nick_a, person_b, nick_b):
    a = initialize(person_a)
    b = initialize(person_b)
    send_key(person_a, a['token'], b['public'], nick_b)
    send_key(person_b, b['token'], a['public'], nick_a)
    m = recieve_msg(person_a, a['token'])
    reply = True
    for i in range(1):
        m = send_msg(person_b, b['token'],m['msg'], m['iv'])
        if m['reply']:
            m = m['reply']
            print m
        else:
            reply = False
        if reply:
            m = send_msg(person_a, a['token'],m['msg'], m['iv'])
            if m['reply']:
                m = m['reply']
                print m
            else:
                reply = False


#communicate(Alice,'alice',Bob,'bob')

'''msg = Eve: I need your help.  My friends Alex and Betty are also using Diffie Hellman to exchange a key and then send encrypted messages.  
        I think that Betty and Bob have a hint; can you find it for me?  I've given you the information I know about their system: 
        http://cs387.udacity-extras.appspot.com/pdf/final_challenge.pdf.  Hopefully you can find a way to break it.  Alex is also trying to help 
        me.  Can you arrange for him and I to exchange messages?  Thanks so much for your help.'''

#communicate(Alex,'alex',Alice,'alice')
#communicate(Alice,'alice',Alex,'alex')
#communicate(Betty, 'betty', Bob, 'bob')
#communicate(Bob, 'bob',Betty, 'betty')
#communicate(Betty, 'betty', Alex, 'alex')
#communicate(Alex, 'alex',Betty, 'betty')

def hex_to_string(hex):
    return ''.join([chr(int(''.join(c), 16)) for c in zip(hex[0::2],hex[1::2])])

def string_to_hex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)
    
    return reduce(lambda x,y:x+y, lst)


def decrypt_communication(person_a, nick_a, person_b, nick_b):
    a = initialize(person_a)
    b = initialize(person_b)
    secret = u'1'
    send_key(person_a, a['token'], secret, nick_b)
    send_key(person_b, b['token'], secret, nick_a)
    m = recieve_msg(person_a, a['token'])
    h = sha1(chr(1)).digest()
    key = h[:16]
    nonce = h[16:]
    reply = True
    i = 0
    while reply and i < 10:
        i+=1
        m = send_msg(person_b, b['token'],m['msg'], m['iv'])
        if 'reply' in m.keys():
            m = m['reply']
            iv = hex_to_string(m['iv'])
            ctr = Counter.new(32, nonce+iv)
            new_key = AES.new(key, AES.MODE_CTR, 'x'*16, counter = ctr)
            print new_key.decrypt(hex_to_string(m['msg']))
        else:
            reply = False
        if reply:
            m = send_msg(person_a, a['token'],m['msg'], m['iv'])
            if 'reply' in m.keys():
                m = m['reply']
                iv = hex_to_string(m['iv'])
                ctr = Counter.new(32, nonce+iv)
                new_key = AES.new(key, AES.MODE_CTR, 'x'*16, counter = ctr)
                print new_key.decrypt(hex_to_string(m['msg']))
            else:
                reply = False

names = [Alex, Alice, Bob, Betty]
nicks = ['alex', 'alice', 'bob', 'betty']


#i = 0
#j = 1
#print nicks[i] + ' to ' + nicks[j]
#decrypt_communication(names[i], nicks[i], names[j], nicks[j])

'''
alex to alice
What is the air-speed velocity of an unladen swallow?
What do you mean?  An African or European swallow?
Ok, good, it is you.  What did you find?
Bob has a PRNG he likes to use to create keys for a OTP. I found 1000 bits and put them online:http://cs387.udacity-extras.appspot.com/final/thousandbits
Thanks.  Anything else?
Also, I think he is using a PRNG similar to the A5.1 GSM
Great news.  I'll look into this

alex to bob
Hi Alex
Are you still using that PRNG?
Yes; but I was only able to use one LFSR

betty to bob
I found a message but don't know what to do with it.
Send it to me
Okay: 8d801f00c7554d3980b0c4f400c1ebc572d86f57f48d322b8e7c3a1f01c531dbe772b77be5acd34bf1979b70089615ace253c4b01350f36f82215f164b7934fdd48a30
Thanks

bob to alice
What is your favorite color
Brown
'''

found_bits = [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0]
found_string = bits_to_string(found_bits)
hexi = '8d801f00c7554d3980b0c4f400c1ebc572d86f57f48d322b8e7c3a1f01c531dbe772b77be5acd34bf1979b70089615ace253c4b01350f36f82215f164b7934fdd48a30'
hexi_string = hex_to_string(hexi)
hexi_bits = string_to_bits(hexi_string)

def lfsr(l, n):
    ans = []
    while len(ans) < n:
        k = (l[0]+l[1]+l[2]+l[5])%2
        ans.append(l[0])
        l = l[1:]+[k]
    return ans

def decrypt_hexi():
    key = lfsr(found_bits[:19], 1000+len(hexi_bits))[1000:]
    m = bits_to_string(xor(key, hexi_bits))
    print m

#decrypt_hexi()
hint = 'An important question: What do you get if you multiply six by nine?'

def final_decrpy_msg(person_a = Alice, nick_a = 'alice'):
    a = initialize(person_a)
    secret = u'1'
    send_key(person_a, a['token'], secret, 'eve')
    secret = 1
    m = recieve_msg(person_a, a['token'])
    h = sha1(chr(1)).digest()
    key = h[:16]
    nonce = h[16:]
    iv = hex_to_string(m['iv'])
    ctr = Counter.new(32, nonce+iv)
    aes = AES.new(key, AES.MODE_CTR, 'x'*16, counter=ctr)
    print aes.decrypt(hex_to_string(m['msg']))
    ctr = Counter.new(32, nonce+iv)
    aes = AES.new(key, AES.MODE_CTR, 'x'*16, counter=ctr)
    hint_enc =  string_to_hex(aes.encrypt(hint))
    m = send_msg(person_a, a['token'], hint_enc, m['iv'])['reply']
    iv = hex_to_string(m['iv'])
    ctr = Counter.new(32, nonce+iv)
    aes = AES.new(key, AES.MODE_CTR, 'x'*16, counter = ctr)
    print aes.decrypt(hex_to_string(m['msg']))

#final_decrpy_msg()

final_answer = 42