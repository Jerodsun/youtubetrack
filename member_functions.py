"""
Supporting calculation and save functions.

For a top-level import, functions such as math will also be imported into that namespace.

"""

import math
import pickle as p

def averagedict(dict1, dict2, a, b):
    """Return a weighted average of the set of two dictionaries. If key only appears in one dictionary, it will still be weighted accordingly."""
    result = {key: ((a * (dict1.get(key, 0)) + (b * dict2.get(key, 0)))) for key in set(dict1) | set(dict2)} #generic combine
    return result



def exponentialdecay(sequence, n, factor = -.1):
    """Recursive function to conduct an exponential decay weighted average of a set of numbers. A factor with greater magnitude decays faster. Visual:
    y = e**(-(factor)x)
    
    For example:
        sequence = [10, 10, 1], n = 3, factor = 0 returns 5.5 as expected.
        sequence = [10, 10, 1], n = 3, factor = -.1 returns 6.169982651304932
        sequence = [10, 10, 1], n = 3, factor = -.5 returns 8.358...
        sequence = [10, 10, 1], n = 3, factor = -1 returns 9.57"""
        
    if n == 0:
        return sequence[0]
    else:
        return ( exponentialdecay(sequence, n - 1) + sequence[n-1] * math.e ** (factor * (n))  ) / ( 1 + math.e ** ((n) * factor))



def picklesave(data, filename = "Pickle.p"):
    """Save data for future reference."""
    with open(filename, "wb") as fp:
        p.dump(data, fp)


def pickleimport(filename = "Pickle.p"):
    """Import an old dataset."""
    data = p.load(open(filename, "rb"))
    return data
    

#res = next(x for x, val in enumerate(cumdates) if val > dt.datetime(2019, 1, 1))
