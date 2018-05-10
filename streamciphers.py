from itertools import chain, islice
from random import Random


def ctr_r(cipher_func, keystream, plainstream, random_class=None):
    random_class = random_class or randbyte
    first_key = next(keystream)
    R = random_class(first_key)
    
    for r, K, P in zip(R, chain([first_key], keystream), plainstream):
        yield Bytes(cipher_func(r, K)) ^ Bytes(P)

def ctr_hr(random_class, keystream, plainstream):
    yield from ctr_r(lambda x,y: Bytes(x) ^ Bytes(y), keystream, plainstream, random_class)

def ichunk(data, size):
    idata = iter(data)
    
    while True:
        to_yield = bytes(islice(idata, size))
        
        if to_yield:
            yield to_yield
        else:
            break

def rchunk(data, size):
    while True:
        to_yield = data.read(size)
        
        if to_yield:
            yield to_yield
        else:
            break

def ihash(hash_function, initial):
    last = initial
    
    while True:
        last = hash_function(last)
        
        yield last

def randbyte(seed):
    r = Random(seed)
    
    while True:
        yield r.randrange(256)


class Bytes(bytes):
    def __init__(self, value=None):
        if isinstance(value, str):
            super().__init__(value, 'utf-8')
        else:
            super().__init__(value)
    
    def __xor__(self, other):
        return self.__class__(x^y for x,y in zip(self, other))

    
    def __or__(self, other):
        return self.__class__(x^y for x,y in zip(self, other))

    
    def __and__(self, other):
        return self.__class__(x^y for x,y in zip(self, other))
