# HW4-Challenge Problem Version 2
#
# Here are 16 intercepted public keys (e, n) and
# associated cipher texts.  Your assignment is to
# decode as many as you can.  Some of them are 
# weak and should be easy to decode (see lecture 22) 
# and some of them are very difficult.
#
# You might also want to research known attacks on
# RSA for ideas on weak keys, messages and padding
#
# Although it is possible to decrypt all 16 message
# only 6 are necessary to get this problem correct.
# Getting at least 11 right would be a double challenge 
# problem. And getting all 16 right means we made a mistake.
#
# To discuss the challenge problem
# http://forums.udacity.com/cs387-april2012/questions/2814/hw4-6-challenge-question-discussion
#
# If you want to use functions from unit4_util, make sure to set the ASCII_BITS = 8
# import unit4_util
# unit4_util.ASCII_BITS = 8
#
# unit4_util code: http://pastebin.com/Te2AmDre
from hashlib import sha512
import math

BITS = ('0', '1')
ASCII_BITS = 8

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

def rev_oaep(cint, g, h):
    cb = convert_to_bits(cint)
    G = cb[:g]
    H = cb[g:]
    nonce = xor(H, hash(G, h))
    mm = xor(G, hash(nonce, g))
    return bits_to_string(mm)
    
    
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

################
e0 = 65537
n0 = 116436872704204817262873499608558046190724591466716177557829773662807162485791977636521167560986434993048860346504247233074117974671540999410485959711510256117299326339754889488213509449940603119123994148576130959569697235313003024809821145961963221161561975123663333322412762102191502543834949106445222007561
cipher0 = "<\xad\xdd\xedg\x8b\x12\x0b\x00y\xa2\xf0\x86\xcbF\xf0\x8f\xb4~\xbd\x04\xd9\xac6iwxk\xcfi\xc4Z1p\\\x14\xa4rL\x9a#\x9f\xbf~\xec[\x8d\xfc(\x82\xc2s\xb9\x0e\xec(\xd9.}\xc5\xdf\xa8'`\xa5\xdb\x18\xf1Z\xff\x82xQJa\x11\x98/x&{\x0b\x17\xb9\xb1\x88\x8f\x85B\x7fH\xdbX\x9aV\x9a\xaf\x0fKc+\xf7?\xb8\xb4\x1fo\x0eeI\xa9\x90\x11\x83\xb8\xfdaMwM\xc7\xb48&-\xe8\xf1C"
m0 = ''#YOUR ANSWER HERE
################

################
e1 = 3
n1 = 131776503472993446247578652375782286463851826883886018427615607890323792437218636575447994626809806013420405963813337101556738852432247872506699457038044621191649758706817663135648397013226104530751563478671698441687437700125203966101608457556637550910814187779205610883544935666685906870199595346450733709263
cipher1 = '\x04\xacq#E/\xf4X\x126\xef\xc6\xb1\xfc\x10p*\x98P\xde\x089K\x16y0\xfa\xde\x9f\x05\x15+\xa3\x0f\xbc3\xd1t\xe7\x9a\x1b\x04m\xa1\x12\x96\x18Y\xf9\xc95\xce\x19 E\xfa\xe1\xb5\x8a\xd5\xf2\x99\xa6"<\xcb\x1a\xd0\xce=\x91\xfbw\t\xb5'
m1 = 'Chinese Remainder Theorem'#YOUR ANSWER HERE
################

################
e2 = 3
n2 = 65659232975830381768328338666607829001259240689809015666589078261348261561917417083788447204534665997091584936794919521220643455263371034991817572752104164283083678838816431044389236958346474896965382016943200300407371205608596328649170408446414718769422147103617311701247139971805834487439320773304455320217
cipher2 = '\x04\xe97r\x13\x99\xf7\x80m\x19\xe3f\x1a\x92]u!\x17\xdf\xa8\xfd\xd4\xd0\xbea\xe8\x1f\xefc\xd6\xc7\xbf\xce\xa4q\xfe\xa4S\xff\xaf\x1aX\xc13g\xeb\x12\xadw\x17T\x05\x1c\x8e\xd8\xea\x1bkc\xd3\xfctQt\x8e\xf6d\x1a\x98\xbc}\x08\x1d%\xc7\xd2K\xb4\xa8\x96\xcf\x98D\x8a\xbd\xa7\xd2\xcc\x861$\xd1\x1b\xdd\xa0h\x83\xdan\xcbm\xa4\xf9\xef\x96\x12\x9c|\xc9\xd7\t\x9b\x0f:\x9e\xe0\xa1\xb2\t\x8b\x9d\x18\x07\x8e]\x8c\x13\xa2'
m2 = 'we recommend you read this blog: http://goo.gl/5I1lt' #YOUR ANSWER HERE
################

################
e3 = 65537
n3 = 123740725722669778168140279746885116465689142044964932919259424632700251889210648897122745920893520079240373449556169792134756802777276891302849411753547670256331297747426561365967232060486102273866172732652784207074573713156422288123095681033001477048754016167961689427177649034193069903791184066398335275979
cipher3 = "\x96\x81\xd11'\xf26\xbfRx\x85\xfa*{l\xa0\xf9gN\xd5\xe1\x89\xe1$$\x0c\r\xa6\xb0\x12^X\x19gQt\xe4\xca\xb2`\xccO\xdf\xb4*\\\x12\x94\xa8\x07\xc8V2\xf2\xfa\xbd\x0f\xd9b%{\x18\x04Q\xebM\xaa\x996\xe7\xb2\xf4;\x8a\xa3\xd6t\xefi^\x9f}\xb6\xa5\xf3\xc7\x86M~b@\x06V\xa62\x99\xd5R\xb7\xaa\x8a\xd2\xd8p\xc6\xf0MU\xaf:(\xea\xa6d6!\xbb\xcd\xf96\xed\x13\xbe\xb4\xc6\x80i'"
m3 = ''#YOUR ANSWER HERE
################

################
e4 = 65537
n4 = 174231520673917075824734399421338044182598066866708821622792727890359025900245087848242723006461374386260651831496339387219798450553867568952404714118529459572066590008168303790157469082308091580819932970387450957047496109838586484814686040623994413943943700280260903054123602347796276801896181827746424409349
cipher4 = '\x8d\x15\x19\xdb\xa2b%\xa8\xf9r\xe1s\xd1\xb9\x91\x01\xac\xa5\xdbU\xac,\xcb\x89\x88\xf1i\xac\xdcC\x9dE\x18\xfeQ\xd9\xb9\xa8\xa8\x16\xafP\xdc\xd5B\x86\xb4)tK\x99\xd3\x7f\x88/\xa2\x90\xdf\xcc\x98\xa1l\xfd\xc7\xfa\x1f\xcd\x82\x1a\xf3\x98*\xb1e\xcd\xb2\xde\xae\xd6\xe8\x93hYEw?\x10\xde\xa9\x18\xc6&H\xebl\xb1\x98\x02)\x06\xf2\r\x9c`\x008\x13\xc1\xa1@\x15\x07\xf5|\x96\xdd\x84\xbd\xf9{\x8ee \xc7\x063\xb5\xb5'
m4 = 'Over the wintry forest, winds howl in rage'#YOUR ANSWER HERE
################

################
e5 = 65537
n5 = 154624207324797376435320332790580937936761022444524329745992492506088072002504225456113354046488778813916771666944276555736671617396500696410754570132980562875859056165807630016963181226874989658340550960200466121814971000456664135187049322544510139273708052345814650574505699754914795663074450228533543056817
cipher5 = "i\xcf\xd3\xcd7.\xc8\xd5\x1f?\xbdtr0&z3\x1d\xf0\xe9p\xf3<YI\x80\xb0\xea3 \xb1\xda\x8e\n\x10m*\xe2\xceE\xbbi\x9c\xb5\x92\xaaMU\xe9\x1a)\x98\x07\x85\x99\xb9V\\\xbfyd\xf4T\xb3\x93\xe3N\xd8\xbd\xd8F\xde\x86Ep\xc0\xef\xd7\xe8\xc4\xf4\x80e\x16x\xcbQ\tV\xc3\xc8\xa4E\x95\xcf\x0e\xd3\\\t\xa2H\xd9\x85$vmC\x9b`\xc0\x93O MG\x0c'\xd6}\xbc\x8fO\xb6V\xcc\x1a\xcb\xc0"
m5 = ''#YOUR ANSWER HERE
################

################
e6 = 65537
n6 = 55658068259817811076952882351578415862870549608181369915628312865059323413004471043604703276316691018017425203301601197751731990108856534305858079813650908006137207122255581819587501300907072084616440442796887872335687503995776108872819766599926331124483312046239535167770356141832350688609707163033799579957
cipher6 = '",G\xae\xb7\x96 z=Y\xf3\x19\x11g\x9eA(\x8e\xa8J\x89\x86u\xb1\xd7\x8f\x86\x1e\x94\xc1GkE\xc8\x03\xe0\xb3LGN\x14\x81\xb2,\xc5\x04Z,\xe4\xf7Z\xdf\x91Z\x97\x1b]\x80\x06\xb4<\xc3x\xab\x83\x85o\x9e\x0bK\xca\x15c\x8c.O\xfb\x84\xbd>\x08\xd7\xff\r\xa6P\x86\x87)\x076\x9b\xdc\xe2\xf1\xe1`/0m\x84f\xb5\x9a\x83\xcc\xd7\x0eC\xae)\xcc\xff\xf3$<\xd6G\x17 \xb1\xd1\xe7\x1a\x0c\xac\x15\x90'
m6 = ''#YOUR ANSWER HERE
################

################
e7 = 65537
n7 = 142790458604757964122637252257956461175023701838768573868119604983049820652820576222661702788815905296939051322350625332330328946814137523526132844748550060162093126006443484056742183764004234747175547357975153233786228275781507259080966207713629148725792124704247615358292708458914175756855275828988145447879
cipher7 = "\xc7\x7f\x91'Y'\xc6_\x91N\xa4\x0e\xe0\x83PX\xe1\xd2O\xf3\xff\x1e\x95\xc5{&\x07\xd7O9\x82;\xf0U9\xf1\x9b\x9a\x8d\x1b+cX\x17-X\xc7\xb0,\xe4Z0\x84PP\x89\xbf\xa4\xc3\xf6\xa2\xec\xdf\xf3\xca\x86\xc4\xad\xcfQ\xcf\xbcW\xd9m\xb2T\x98\x9dWu\xab\x8f\xe3\x91\xccL@\x89\xcf\xcc\x1f\xed>\x98\\\x02\xefE\x84\xa3t\x1d\xd3\xf8(PkO\x17q\xf7\xafX\x10S\x94\xdf\x9a*\xbc\xb3\x00\xecYa\xc2\x16"
m7 = ''#YOUR ANSWER HERE
################

################
e8 = 3
n8 = 105242314862613403128618012971241387248892052783002974105856821061278607957729115063535600558210614458208545471459242061573520534172108013775924181710251914675571061791713994144059933046151548906145029415704879628926489802957314522493622596489433179478769931611554984108813301116133814976882152241405085792401
cipher8 = '!t\x1fF\x81\xc3\x84m\x96z_\xaf\xcf[\xbbt\xef\xac\xf7\xc9]\xebaw\x06\x0e\x8ey\\H_\xee0B\xbaB?\xa9-4\x1cd\x16\xa4\x85\xeaOO\xda\xf8\x8e;\xdbY\xb6b\xf7|\xaf\x13\xa9\xba\x9a\xc5i\xa7f\x94\x80HJ^-\x80\x96\xd9\xb5\x1e\x9b5\x1c\xe2\xfa\xbc\xb3\xb5\xfa\xffIq\xabt$\x10\x01K\xef[;\x04T\x17\n\xbf\xa7\xb4\x0fr2\x19\xc43\x19\xa9\xac\xbb\x82Y\xf4X%\x8f\x0bd\x81\xa7n\xce'
m8 = 'we recommend you read this blog: http://goo.gl/5I1lt' #YOUR ANSWER HERE
################

################
e9 = 3
n9 = 72119364642335338558230934777058054962694972953443182639333046521176125046406938854054638169330108689724380250570350428800376971990405399883726478777738596059986080075671524555383338963957060973245384873014181662159740775682510335778372893164426839838949550467826086219705472573462606617295335262085826901917
cipher9 = 'B\xc1\xd9EH\x8b\xc9D_s\x17\x90uGd\xb6\x10F\x16\xab\x1aN=t\\\xb6\xaa\xf6\x97\xd6\x17\xab&\xd1 Z\x82\xac\xc0wVw|\xa8\xf4\x8dxG\xb7Og\x8b\x8au?\x8c\xe3(\x0c\xec+\x0c\xc3\x8a\xe8k\x8f\x00\xc1\xf8\x95*\xe5\n\xc8fm\xdd\xcbIB\x97"B\x1d}\xa2m8v\x9a\xcf.:\x9f\xf2\xd9@\x11.\x92\xd0\x1dkHzet\xd7\xe6\xc0j\xab\xad\xff\xb3\xe6$\x97\xfd=\x0b\x1c%_\xd1\xa9"'
m9 = '###Should you use a random nonce with oaep?'#YOUR ANSWER HERE
################

################
e10 = 65537
n10 = 98326993759634789515778687799020543645398962489890436310231025647956456166685176265303236823165224008000474960054742885390051491705558213022700710136581245927093740780985394183390749017153700221212481058983678953171251665248666951370742484457781880038452217032906924859256620548427923611534146579043548158531
cipher10 = '?+\xdfn\x17R\xfc;\x84\xcc<)\xceC\xad\x12y\xaa\x85#\xf1G\xd0\x1fF\xd1F\xc4\xdb\x00\xd0\x8c\xc7\xc1\xa0\xc6}P\xd3\xf0\nHB\xdb\x1b\xd3A\xab8\x0f\xcf\xc6\xe9N\x01\x03\x96\n\xb7\x1bU[\xd3\xf2\xe1z\xe2Y\xb0bH\x0f\xd1\x12\x80\xe3\xb7\x1b\x1aU\xd8\xf3\x8c\xcc\xa1\xad\x8dK\xc8\xba\xc4\xcd\x18j"A\xb6\x1b\xd0\xc4\xd5\x9aVT]biR\xb0\xa8p\xc1U$\t\x97\xfe\r(\x95\xc5V\xff]#\xa2\xe3\xf6'
m10 = ''#YOUR ANSWER HERE
################

################
e11 = 65537
n11 = 59271838373237712241010698426785545947980750376894660532845611609385295493574642459966039842508102834600550821189433548722152899983884277266737416092985257305168009937861700509240511070647418413603755912503843488856979904991517729100725512850421664634705274281314737938901139871448406073842088742598680079967
cipher11 = 'J\xc1R\x90\xe1\xf4\x8b5My\xf8\xa1\xf4>\xa2\xc3\x10\xbd\xeb\xcc&\x7fb\x1aC$\x1d\xc5\xb7\xcdz\xb7\x17\x8a#9\x12\x89\xfeao\x19\x9c\xeb\xb0>\x86\x9b\x1d3~b0-u\xfc\x04!\rc\\\xcb$\x91\x9e\xa1N\x9d2\xff\x19\x9a9vH.\xd5\xe7m\xa9m\xea^\xd3T$\xd7\xd7\x11\x81\xe4B\x9b~\x8c $\xa6K\x8a\xdc`\xb4\x9cu\xfb\xc2\x06\xd1\xbb\xb9\xa0\x8f\xd2\xbc\x02\xf6#\x1f\x1dM\xbb\x98\xf2\xa0\x9fO\x80'
m11 = 'What could go wrong: http://pastebin.com/hNz9gZbe' #YOUR ANSWER HERE
################

################
e12 = 65537
n12 = 72216220929585874029800250341144628594049328751082632793975238142970345801958594008321557697614607890492208014384711434076624375034575206659803348837757112962991028175041084288364853207245546083862713417245642824765387577331828704441227356582723560291425753389466410790421096831823015438162111864463275922441
cipher12 = ".\xfd9\x8dc\xda\xf9o\xf5Vl\xfb\x87\xed\xd5 \xee\xcf\x97~\xd8T\xf9.\x18\xb1\xd5n^\xa0\rA\xe0\x1d\xd5\xc8:D\xc9\x14o\xde\xdbo\xf9>)bc'a\xa2\x8e\xc1|\xdd\r[q1\xac\x0f^\x82b/A\x10\x87\xff\xe4k=\xc8\xd6\x1c\x7f\xfb\xdb\xda&\xd9\xc5\xc4\x8a#\xa0u\x03J&\n\x83\xa0\xe1.\xba\xfd\x8a0s?\xdeg\xd50\x15\xeb\x91\xb3E\xc7\x15O\xf3r\xe3`~8\xb4\xb5=\x89U\x7f\xfa\x19"
m12 = 'A real example: http://digitaloffense.net/tools/debian-openssl' #YOUR ANSWER HERE
################

################
e13 = 3
n13 = 70312356315714780126407430932110548424144037560501611854827137092512910875581601526352040261858471208166388560443445258525272960150598064892138505585965821412085549228607722662540954787033730390722435251172318708904239583536234789288179180688257614871029465697421428231000338910272301520713624044424711448629
cipher13 = '&\xb91\x8ex\x91!0\x855jX\xd1Y\xfc\x9a \xf1\xd9\x9a\xa4\x84s\x0c\xf0\x96\x9e\xcc\xa4L\xe6o\x12\x11~\xd8\xef\x11-t\xf5\xfce\x8a\xb1\xc2mL\xa8\xaa\xb71\xd4y\xa4\xd1\x15\xfdn\x1a\x16\xdf\xfb\xe7\x83Zi\x8f\xb7\x151K\xc72\xf6\xe6\xb31c\xc9\x18\xe9\x92u]\x9f\x01j\x12\xd2\xd3Y("\x9bm9\xc3\x1a9\x1e\xb4\xd4\xa3\xfei\x97\x8a\xa3k\xdc}\xfcy\xf4z\x96\x98\xbev\xce\xa5j\xfdk!xV'
m13 = 'we recommend you read this blog: http://goo.gl/5I1lt' #YOUR ANSWER HERE
################

################
e14 = 65537
n14 = 99428965906962816070784007311850456823957258033424536090292194626620222742187661756726403412281396587119713030320975423136670466362256289782688266974070489861007966741029067535118700826392643025215295741522514598507712664582141077802475427001379922637288480239204598457282788664201418160351588075772782828233
cipher14 = ':\xba\xb7\x0f`\x959\xc2\x900\xf0b\xb3\xe6\xde\xe6\x80\xdf\xc9\x1b\xed\xa6G\x90\x0c\xc2\xa4Z\xc1\x85n\xb6K/\x97\xd4\x9b\x0cKC\x1b\x9e\x83\x13{\x8a\xa6\xa3\x01\xed\x142\xf3\xab\xbb\x1f\x96bQO\x00\x1c\xc5\xba\xfc\xaf\xf2=\x9c\xaa\x94&3aN\r\xe2xh\xad\x18\xf4X\xc1;\xe8\xbcmOn]\xd2JO:+z\xbd\xa6_Q\x10\xf8\xde\xf6`\xdfF\xfa<\xe3 N%$ev\x08\xdai\x85\x8f\x17\xfb,\xa9s\x85'
m14 = ''#YOUR ANSWER HERE
################

################
e15 = 65537
n15 = 118399170574854942444633896245235023966560880236530051363584486215325592633889564680653306117442159965072738319247448982717567259059972729844114596818478915558131833772330699563816353891596654144981880987927436049203299944850160662951894970183034856877612682945727163824998131146307156333199771146520933436033
cipher15 = '@\xc4X\x1a\xae\xb6C\x12.\xfcvK\x90s\xbe\xf2\xab\xda#j\xba\xf7\x81\xee\xa2\xb2\xddR~Z\xbak(u\xee\x90\xf9\xbc\xe3m\xc8\xdb\xf37k\xe8\xb0\xac\xc2T\xe9\x97\xe4\x01~\xdd\xd4A\xd3\xe9\\\x876}#\xddK7n\xae\x1e\xed\xe6z\x82Zp\xe5c\xc0C\xbd\xf9\x8bD\x03\x19\x9d\xb5s \x0f\xe1c\xd4\xf5M\xc4\xbc\x971\x87\xd6\xb5\x1d\x10\xb7\xc4/\xf6\x8d!u\xed\xe9|U\xbe\x98\xbaLLp\x8ehZ\xec\x1d'
m15 = ''#YOUR ANSWER HERE
################
import gmpy2
import gmpy

not_found = [0,3,5,6,7,10,14,15]

es = [e0,e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,e13,e14,e15]
ns = [n0,n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15]
cs = [bits_to_int(string_to_bits(cipher0)),
                  bits_to_int(string_to_bits(cipher1)),
                  bits_to_int(string_to_bits(cipher2)),
                  bits_to_int(string_to_bits(cipher3)),
                  bits_to_int(string_to_bits(cipher4)),
                  bits_to_int(string_to_bits(cipher5)),
                  bits_to_int(string_to_bits(cipher6)),
                  bits_to_int(string_to_bits(cipher7)),
                  bits_to_int(string_to_bits(cipher8)),
                  bits_to_int(string_to_bits(cipher9)),
                  bits_to_int(string_to_bits(cipher10)),
                  bits_to_int(string_to_bits(cipher11)),
                  bits_to_int(string_to_bits(cipher12)),
                  bits_to_int(string_to_bits(cipher13)),
                  bits_to_int(string_to_bits(cipher14)),
                  bits_to_int(string_to_bits(cipher15))]

def eth_root(n,e,c):
    if e <> 3:
        return None
    for k in range(32):
        c = gmpy.mpz(c) + k * gmpy.mpz(n)
        (m,r) = gmpy.root(c,e)
        if r == 1:
            mb = convert_to_bits(m)
            return bits_to_string(pad_bits(mb, len(mb) + pad(len(mb))))
    return None

def pad(p):
    if p % 8:
        return 8 - (p % 8)
    else:
        return 0    

def check_eth():
    for i in range(16):
        print i, eth_root(ns[i], es[i], cs[i])

#check_eth()

##0 None
##1 Chinese Remainder Theorem
##2 None
##3 None
##4 None
##5 None
##6 None
##7 None
##8 None
##9 ###Should you use a random nonce with oaep?
##10 None
##11 None
##12 None
##13 None
##14 None
##15 None

def find_p_q():
    for i in range(16):
        for j in range(16):
            if i <> j:
                n1 = gmpy.mpz(ns[i])
                n2 = gmpy.mpz(ns[j])
                p = gmpy.gcd(n1,n2)                
                if p <> 1:
                    q = n1/p
                    print i
                    print 'p', p
                    print 'q', q

#find_p_q()
p11 = 7924057187763558064452801291482013694582305119032293927979457583171139106404218548653442118775641945544367293470393031489286439304696105851789091398057521
q11 = 7479986195047422044783207980234740836617869092231627658933586047604001576736255695849351325981066613538650908773276048784366105940806290259977144299798927
tot11 = (p11-1)*(q11-1)
#d11 = gmpy.invert(e11,tot11)
d11 = long(19327085250104367160388767038167861160998346515010435259272025269581515246314144824594874215090684004080348063671181087571790095253911637780035378212415805108977116464004449479056892823789477695820519235549427392543620716616755957076886326577621748361715429563341532303066541207225850152002693562184368068673)

p12 = 7924057187763558064452801291482013694582305119032293927979457583171139106404218548653442118775641945544367293470393031489286439304696105851789091398057521
q12 = 9113541108853074739983367581944803253574657343701000849714566262760998409185399558785268448671978721129827908801927097302433549828876086034343525863474521
tot12 = (p12-1)*(q12-1)
#d12 = gmpy.invert(e12,tot12)
d12 = long(34974790611487490146113797485816111686148674711374685519336772489706254112244469136886434248169547804205604198797179317295452304249468499616737999788064913326395246954603945900921622873045816839339822645354539561617659212635114488983106126207519950809007021585149514854922833883906913810914368444219181481473)

#print decrypt(cipher11, n11, d11, 512, 512)

'''
What could go wrong: http://pastebin.com/hNz9gZbe
'''

#print decrypt(cipher12, n12, d12, 512, 512)

'''
A real example: http://digitaloffense.net/tools/debian-openssl
'''

import gmpy2
from gmpy2 import mpz

def chinrest(aas,ns):
    count=len(aas)
    m = 1
    ms = [1]*count
    ees = [mpz(0)] * count

# product of all ns
    for i in range(0,count):
        m = gmpy2.mul(m ,ns[i])

# products of all but one ns
    for i in range(0,count):
        ms[i] = gmpy2.div(m , ns[i])

# extended euclid to get the factors        
    for i in range(0,count):
        ggtn,r,s = gmpy2.gcdext(mpz(ns[i]),mpz(ms[i]))
        ees[i] = gmpy2.mul(s , ms[i])

# calculating x    
    x = 0
    for i in range(0,count):
        x = gmpy2.add(x ,gmpy2.mul(aas[i] , ees[i]))

# making x positive. just in case     
    x = gmpy2.t_mod(mpz(x),mpz(m))
    while x < 0:
        x = gmpy2.t_mod(mpz(x+m),mpz(m))
 
    return m, x

def find_cube(i,j,k):
    n,x = chinrest([cs[j],cs[k],cs[i]],  [ns[j],ns[k],ns[i]])
    n = long(n)
    x = long(x)
    for i in range(100):
        x += n
        (m,r) = gmpy.root(x,3)
        if r == 1:
            z = m
            pass
    return rev_oaep(z,512,512)

#m = find_cube(2,8,13)

'''
we recommend you read this blog: http://goo.gl/5I1lt
'''
#non = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]



import random
import os
from Crypto.Util import number

random.seed(os.getpid())

def randfunction(N):
    # N is in bytes
    # pycrypto expects a string
    l = []
    while N > 0:
        l.append(chr(random.getrandbits(8)))
        N -= 1
    return "".join(l)

#p = number.getPrime(512, randfunction)
#q = number.getPrime(512, randfunction)
#n = p*q

def no_rand(n=0):
    for i in range(n,50000):
        random.seed(i)
        p = number.getPrime(512, randfunction)
        q = number.getPrime(512, randfunction)
        n = p*q
        print i
        if n in ns:
            print 'i',i
            print 'p',p
            print 'q',q
            print 'n',n
            return p,q,n

def no_rand2(n=0):
    random.seed(22409)
    for i in range(n,50000):        
        print i
        p = number.getPrime(512, randfunction)
        if p == gmpy.gcd(p, n10):
            print 'success'
            return p


#p,q,n = no_rand(11200)
p4 = 13042679636962606212055287647645266033317379914206304459842576373826530575608359124296602149372820388703575422136195969224054407851739993913185190047083179
q4 = 13358567834492353350561903537665742939596579878030661994595241880015059611860680118069347091505462570105435227114865482311624428970113317094373033033705231
tot = (p4-1)*(q4-1)
d4 = gmpy.invert(es[4],tot)
m = decrypt(cipher4, ns[4], d4, 512, 512)

'''
Over the wintry forest, winds howl in rage
'''

#p = no_rand2()

def find_close(n):
    sq = gmpy.sqrt(n)
    sq = sq - 10
    if sq%2 == 0:
        sq = sq-1
    for i in range(10000):
        sq = sq + 2
        if sq == gmpy.gcd(sq,n):
            return sq
    return None


#p0 = find_close(n0)
p0 = 10790591860699987445470091071758055654466628106694684328230290421283239835254521042012386422016381436076520219519026385088167825285749984974093329105227383
#q0 = n0/p0
q0 = 10790591860699987445470091071758055654466628106694684328230290421283239835254521042012386422016381436076520219519026385088167825285749984974093329105226367
#tot0 = (p0-1)*(q0-1)
tot0 = 116436872704204817262873499608558046190724591466716177557829773662807162485791977636521167560986434993048860346504247233074117974671540999410485959711510234536115604939779998548031365933829294185867780759207474498988854668833332515767737121189119188398689822083224295269642585766540931043865000919787011553812
#d0 = gmpy.invert(e0, tot0)
d0 = 88978614504356098969425372040157530392356516011353580488139993050959127082616442986286420095355640894790317284490069883070906150838459440201351264694323139082315970010742967900308327642370549634811330942561129405654207844797762470889418351517363736414287862880083604005283122211268488159953110091471582657705
#m0 = decrypt(cipher0,n0,d0,256,256)


#p6 = find_close(n6)
p6 = 7460433516882099464591943619576719398475399816355435827205888362722682480669316041986494290174286891088521313357518338919813231136870653904576096378253799
#q6 = n6/p6
q6 = 7460433516882099464591943619576719398475399816355435827205888362722682480669316041986494290174286891088521313357518338919813231136870653904576096378253443
#tot6 = (p6-1)*(q6-1)
tot6 = 55658068259817811076952882351578415862870549608181369915628312865059323413004471043604703276316691018017425203301601197751731990108856534305858079813650893085270173358056652635700262147468275133816807731925233460558962058630814770240735793611345982550701135003612820131092516515370076947301898010841043072716
#d6 = gmpy.invert(e6,tot6)
d6 = 43351416030496665764898253391499028276181242279921665756948942711900426063753699877807127018979535372472305520968819670421821431666031259443929864689680996817533626336807603192730146048486588835021633084881142976146188828369754043696058704559024169938860340531217785623567581641570119899476214746805497424201
m6 = decrypt(cipher6,n6,d6,512,512)

mint = bits_to_int(string_to_bits(m6))
for i in range(10):
    m = mint + i*n6
    print m
    raw_input()
    m1 = convert_to_bits(m)
    print m1
    raw_input()
    while len(m1) < 1024:
        m1+=[0]
    print len(m1)
    raw_input()
    m2 = bits_to_string(m1)
    print m2