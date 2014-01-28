import sys
import decimal

def reducer():
    sales_total = 0
    old_key = None
    decimal.getcontext().prec = 2
    for line in sys.stdin:
        data = line.strip().split('\t')
        if len(data) <> 2:
            continue
        else:
            this_key, this_sale = data
            if old_key and old_key <> this_key:
                print '{0}\t{1}'.format(old+key, sales_total)
                sales_total = 0
            else:
                old_key = this_key
                sales_total += decimal.Decimal(this_sale)
    if old_key <> None:
        print '{0}\t{1}'.format(old+key, sales_total)