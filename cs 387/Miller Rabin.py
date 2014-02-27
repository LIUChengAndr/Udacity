import random



def mod_exp(a, b, q):
    """returns a**b % q"""
    if b == 0:
        return 1
    elif b%2 == 0:
        return (mod_exp(a, b/2, q)**2) % q
    elif b%2 == 1:
        return (a * mod_exp(a,b-1,q)) % q




def rabin_miller(n, target=128):
    """returns True if prob(`n` is composite) <= 2**(-`target`)"""
    if n%2 == 0:
        return False
    t,s = make_ts(n)
    iterations = target/2
    test_nums = []
    if iterations > n:
        return 'n too small'
    while len(test_nums) < iterations:
        new_num = random.randint(1,n)
        if new_num not in test_nums:
            test_nums.append(new_num)
        a = new_num
        for a in test_nums:
            test_one = True
            test_two = True
            if mod_exp(a,s,n) <> 1:
                test_one = False
            if not test_one:
                test_two = False
                for j in range(t):
                    if mod_exp(a, 2**j*s, n) == n-1:
                        test_two = True
            if not test_one and not test_two:
                return False
    return True


def make_ts(n):
    old_n = n
    n -= 1
    t = 0
    while n%2 == 0:
        n = n/2
        t+=1
    s = (old_n-1)/(2**t)
    return t, s

print rabin_miller(101)
