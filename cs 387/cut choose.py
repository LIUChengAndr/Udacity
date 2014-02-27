from Crypto.Util.number import GCD
import random
import re

def create_bill(bill_number, bill_amount):
    return "Bill %d. IPBank %d" % (bill_number, bill_amount)

def bill_value(bill):
    m = re.match("Bill \d*. IPBank (\d*)", bill)
    return int(m.group(1))

BANK_PUBLIC_KEY = (65537L, 146605267664968305757478488924026371034279663748432168896352333338344662802484320667649241137968415481826877512428632071426825921963704188324773006253432133951867548217268558652196457406282093300704326236710745110041671406733381071035768220531466030063347486543092022483351958440259179724216272703778522201967L)

#########
# Code for Alice
def random_nonce(bits=50):
    while True:
        test = random.getrandbits(50)
        if GCD(test, BANK_PUBLIC_KEY[1]) == 1:
            return test

def create_bill_message(i, bill_amount, nonce):
    bill = create_bill(i, bill_amount)
    bill_int = bits_to_int(string_to_bits(bill))
    t = blind_msg(bill_int, nonce, BANK_PUBLIC_KEY[0], BANK_PUBLIC_KEY[1])
    return t

def blind_msg(msg, nonce, e, n):
    return (msg * pow(nonce, e, n)) % n

_NONCES = None
def generate_bills(bill_amount, bill_count=100):
    """
    generates a set of bills of to be sent to the bank
    """
    global _NONCES
    _NONCES = []
    bills = []
    cheat_i = None
    for i in range(bill_count):
        nonce = random_nonce()
        t = create_bill_message(i, bill_amount, nonce)
        _NONCES.append(nonce)
        bills.append(t)
    return bills

def cheat_generate_bills(bill_amount, cheat_amount, bill_count=100):
    i = random.randint(0, bill_count-1)
    bills = generate_bills(bill_amount, bill_count)
    i = random.randint(0, bill_count-1)
    t = create_bill_message(i, cheat_amount, _NONCES[i])
    bills[i] = t
    return bills

def send_nonces(select_bill):
    return [n for i,n in enumerate(_NONCES) if i != select_bill]

##########
# Code for the bank
_BANK_PRIVATE_KEY = 40160586697425515254955388736943183837807998585159569833776545164156151964432320810325569161694111160798296107246764904989941647878517193234274528606250921861797675796157384299290208363046057168831417657336178672805630150267562009631690725301405637880870922628396388936009628239314530865889540780573312928073L
_ALL_BILLS = None
_SIGNED_BILL = (None, None)

def sign_bill(bill):
    return pow(bill, _BANK_PRIVATE_KEY, BANK_PUBLIC_KEY[1]) 

def pick_and_sign_bills(bills):
    global _ALL_BILLS
    global _SIGNED_BILL
    choosen = random.randint(0, len(bills)-1)
    signature = sign_bill(bills[choosen])
    _SIGNED_BILL = (choosen, signature)
    _ALL_BILLS = [b for i,b in enumerate(bills) if i != choosen]
    return choosen # return the index of the choosen bill

def verify_bills_and_return_signed(nonces, value):
    if not _verify(_ALL_BILLS, nonces, value):
        return None
    return _SIGNED_BILL[1]

# This will be changed by the student
#_verify = None
#Code for unit6_util: http://pastebin.com/Tnn44HjN

# Below are the typical bit manipulation functions
# that you might find useful

BITS = ('0', '1')
ASCII_BITS = 8

def pad_to_block(bits, block_size):
    if len(bits) % block_size == 0:
        return bits
    else:
        return pad_bits(bits, block_size * (len(bits) / block_size + 1))

def display_bits(b):
    """converts list of {0, 1}* to string"""
    return ''.join([BITS[e] for e in b])

def seq_to_bits(seq):
    return [0 if b == '0' else 1 for b in seq]

def pad_bits(bits, pad):
    """pads seq with leading 0s up to length pad"""
    assert len(bits) == 0
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

# In this assignment, you will write the verify step
# for the bank in the cut-and-choose protocol.  
# 
# The code for the cut-and-choose protocol
# is in the `cutchoose` module
# 1) Alice generates N bills 
# for some amount.
# 2) The bills are sent to the bank.  The bank
# picks one and signs it.
# 3) Before sending it back to Alice, the bank
# asks for the random nonces for the other N-1 bills
# 4) The bank verifies the nonces and the amounts
# before sending back the signed bill
# This last step is where you will be adding your code
#


def _verify(bills, nonces, value):
    print bills
    print nonces
    print value
        
    ###########
    ### Your code here
    # Return True if all of the bills
    # have the value specified
    # or False otherwise
    
    return True
    ###########
cutchoose._verify = _verify

def test():
    # Alice generates some bills
    bills = cutchoose.generate_bills(50)
    # and sends them to the bank.
    # The bank picks one and sends
    # back which one
    i = cutchoose.pick_and_sign_bills(bills)
    # Alice now needs to send back 
    # the random nonces
    nonces = cutchoose.send_nonces(i)
    # bank checks the nonces and
    # if they pass, returns the signed bill
    signed = cutchoose.verify_bills_and_return_signed(nonces, 50)
    assert signed is not None
    assert bills[i] == pow(signed, cutchoose.BANK_PUBLIC_KEY[0], 
                           cutchoose.BANK_PUBLIC_KEY[1])

    # here, we'll try to cheat and see if we get caught
    bills = cutchoose.cheat_generate_bills(50, 100)
    i = cutchoose.pick_and_sign_bills(bills)
    nonces = cutchoose.send_nonces(i)
    signed = cutchoose.verify_bills_and_return_signed(nonces, 50)
    # there is a 1% chance we got away with this
    assert signed is None
    
test()
