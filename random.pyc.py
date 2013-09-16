# 2013.08.22 22:13:24 Pacific Daylight Time
# Embedded file name: random
from warnings import warn as _warn
from types import MethodType as _MethodType, BuiltinMethodType as _BuiltinMethodType
from math import log as _log, exp as _exp, pi as _pi, e as _e
from math import sqrt as _sqrt, acos as _acos, cos as _cos, sin as _sin
from math import floor as _floor
from os import urandom as _urandom
from binascii import hexlify as _hexlify
__all__ = ['Random',
 'seed',
 'random',
 'uniform',
 'randint',
 'choice',
 'sample',
 'randrange',
 'shuffle',
 'normalvariate',
 'lognormvariate',
 'expovariate',
 'vonmisesvariate',
 'gammavariate',
 'gauss',
 'betavariate',
 'paretovariate',
 'weibullvariate',
 'getstate',
 'setstate',
 'jumpahead',
 'WichmannHill',
 'getrandbits',
 'SystemRandom']
NV_MAGICCONST = 4 * _exp(-0.5) / _sqrt(2.0)
TWOPI = 2.0 * _pi
LOG4 = _log(4.0)
SG_MAGICCONST = 1.0 + _log(4.5)
BPF = 53
RECIP_BPF = 2 ** (-BPF)
import _random

class Random(_random.Random):
    __module__ = __name__
    VERSION = 2

    def __init__(self, x = None):
        self.seed(x)
        self.gauss_next = None
        return

    def seed(self, a = None):
        if a is None:
            try:
                a = long(_hexlify(_urandom(16)), 16)
            except NotImplementedError:
                import time
                a = long(time.time() * 256)

        super(Random, self).seed(a)
        self.gauss_next = None
        return

    def getstate(self):
        return (self.VERSION, super(Random, self).getstate(), self.gauss_next)

    def setstate(self, state):
        version = state[0]
        if version == 2:
            version, internalstate, self.gauss_next = state
            super(Random, self).setstate(internalstate)
        else:
            raise ValueError('state with version %s passed to Random.setstate() of version %s' % (version, self.VERSION))

    def __getstate__(self):
        return self.getstate()

    def __setstate__(self, state):
        self.setstate(state)

    def __reduce__(self):
        return (self.__class__, (), self.getstate())

    def randrange(self, start, stop = None, step = 1, int = int, default = None, maxwidth = 1L << BPF):
        istart = int(start)
        if istart != start:
            raise ValueError, 'non-integer arg 1 for randrange()'
        if stop is default:
            if istart > 0:
                if istart >= maxwidth:
                    return self._randbelow(istart)
                return int(self.random() * istart)
            raise ValueError, 'empty range for randrange()'
        istop = int(stop)
        if istop != stop:
            raise ValueError, 'non-integer stop for randrange()'
        width = istop - istart
        if step == 1 and width > 0:
            if width >= maxwidth:
                return int(istart + self._randbelow(width))
            return int(istart + int(self.random() * width))
        if step == 1:
            raise ValueError, 'empty range for randrange() (%d,%d, %d)' % (istart, istop, width)
        istep = int(step)
        if istep != step:
            raise ValueError, 'non-integer step for randrange()'
        if istep > 0:
            n = (width + istep - 1) // istep
        elif istep < 0:
            n = (width + istep + 1) // istep
        else:
            raise ValueError, 'zero step for randrange()'
        if n <= 0:
            raise ValueError, 'empty range for randrange()'
        if n >= maxwidth:
            return istart + self._randbelow(n)
        return istart + istep * int(self.random() * n)

    def randint(self, a, b):
        return self.randrange(a, b + 1)

    def _randbelow(self, n, _log = _log, int = int, _maxwidth = 1L << BPF, _Method = _MethodType, _BuiltinMethod = _BuiltinMethodType):
        try:
            getrandbits = self.getrandbits
        except AttributeError:
            pass
        else:
            if type(self.random) is _BuiltinMethod or type(getrandbits) is _Method:
                k = int(1.00001 + _log(n - 1, 2.0))
                r = getrandbits(k)
                while r >= n:
                    r = getrandbits(k)

                return r

        if n >= _maxwidth:
            _warn('Underlying random() generator does not supply \nenough bits to choose from a population range this large')
        return int(self.random() * n)

    def choice(self, seq):
        return seq[int(self.random() * len(seq))]

    def shuffle(self, x, random = None, int = int):
        if random is None:
            random = self.random
        for i in reversed(xrange(1, len(x))):
            j = int(random() * (i + 1))
            x[i], x[j] = x[j], x[i]

        return

    def sample(self, population, k):
        n = len(population)
        if not 0 <= k <= n:
            raise ValueError, 'sample larger than population'
        random = self.random
        _int = int
        result = [None] * k
        if n < 6 * k:
            pool = list(population)
            for i in xrange(k):
                j = _int(random() * (n - i))
                result[i] = pool[j]
                pool[j] = pool[n - i - 1]

        else:
            try:
                n > 0 and (population[0], population[n // 2], population[n - 1])
            except (TypeError, KeyError):
                population = tuple(population)

            selected = {}
            for i in xrange(k):
                j = _int(random() * n)
                while j in selected:
                    j = _int(random() * n)

                result[i] = selected[j] = population[j]

        return result

    def uniform(self, a, b):
        return a + (b - a) * self.random()

    def normalvariate(self, mu, sigma):
        random = self.random
        while True:
            u1 = random()
            u2 = 1.0 - random()
            z = NV_MAGICCONST * (u1 - 0.5) / u2
            zz = z * z / 4.0
            if zz <= -_log(u2):
                break

        return mu + z * sigma

    def lognormvariate(self, mu, sigma):
        return _exp(self.normalvariate(mu, sigma))

    def expovariate(self, lambd):
        random = self.random
        u = random()
        while u <= 1e-07:
            u = random()

        return -_log(u) / lambd

    def vonmisesvariate(self, mu, kappa):
        random = self.random
        if kappa <= 1e-06:
            return TWOPI * random()
        a = 1.0 + _sqrt(1.0 + 4.0 * kappa * kappa)
        b = (a - _sqrt(2.0 * a)) / (2.0 * kappa)
        r = (1.0 + b * b) / (2.0 * b)
        while True:
            u1 = random()
            z = _cos(_pi * u1)
            f = (1.0 + r * z) / (r + z)
            c = kappa * (r - f)
            u2 = random()
            if not (u2 >= c * (2.0 - c) and u2 > c * _exp(1.0 - c)):
                break

        u3 = random()
        if u3 > 0.5:
            theta = mu % TWOPI + _acos(f)
        else:
            theta = mu % TWOPI - _acos(f)
        return theta

    def gammavariate(self, alpha, beta):
        if alpha <= 0.0 or beta <= 0.0:
            raise ValueError, 'gammavariate: alpha and beta must be > 0.0'
        random = self.random
        if alpha > 1.0:
            ainv = _sqrt(2.0 * alpha - 1.0)
            bbb = alpha - LOG4
            ccc = alpha + ainv
            while True:
                u1 = random()
                if not 1e-07 < u1 < 0.9999999:
                    continue
                u2 = 1.0 - random()
                v = _log(u1 / (1.0 - u1)) / ainv
                x = alpha * _exp(v)
                z = u1 * u1 * u2
                r = bbb + ccc * v - x
                if r + SG_MAGICCONST - 4.5 * z >= 0.0 or r >= _log(z):
                    return x * beta

        elif alpha == 1.0:
            u = random()
            while u <= 1e-07:
                u = random()

            return -_log(u) * beta
        else:
            while True:
                u = random()
                b = (_e + alpha) / _e
                p = b * u
                if p <= 1.0:
                    x = pow(p, 1.0 / alpha)
                else:
                    x = -_log((b - p) / alpha)
                u1 = random()
                if not (p <= 1.0 and u1 > _exp(-x) or p > 1 and u1 > pow(x, alpha - 1.0)):
                    break

            return x * beta

    def gauss(self, mu, sigma):
        random = self.random
        z = self.gauss_next
        self.gauss_next = None
        if z is None:
            x2pi = random() * TWOPI
            g2rad = _sqrt(-2.0 * _log(1.0 - random()))
            z = _cos(x2pi) * g2rad
            self.gauss_next = _sin(x2pi) * g2rad
        return mu + z * sigma

    def betavariate(self, alpha, beta):
        y = self.gammavariate(alpha, 1.0)
        if y == 0:
            return 0.0
        else:
            return y / (y + self.gammavariate(beta, 1.0))

    def paretovariate(self, alpha):
        u = 1.0 - self.random()
        return 1.0 / pow(u, 1.0 / alpha)

    def weibullvariate(self, alpha, beta):
        u = 1.0 - self.random()
        return alpha * pow(-_log(u), 1.0 / beta)


class WichmannHill(Random):
    __module__ = __name__
    VERSION = 1

    def seed(self, a = None):
        if a is None:
            try:
                a = long(_hexlify(_urandom(16)), 16)
            except NotImplementedError:
                import time
                a = long(time.time() * 256)

        if not isinstance(a, (int, long)):
            a = hash(a)
        a, x = divmod(a, 30268)
        a, y = divmod(a, 30306)
        a, z = divmod(a, 30322)
        self._seed = (int(x) + 1, int(y) + 1, int(z) + 1)
        self.gauss_next = None
        return

    def random(self):
        x, y, z = self._seed
        x = 171 * x % 30269
        y = 172 * y % 30307
        z = 170 * z % 30323
        self._seed = (x, y, z)
        return (x / 30269.0 + y / 30307.0 + z / 30323.0) % 1.0

    def getstate(self):
        return (self.VERSION, self._seed, self.gauss_next)

    def setstate(self, state):
        version = state[0]
        if version == 1:
            version, self._seed, self.gauss_next = state
        else:
            raise ValueError('state with version %s passed to Random.setstate() of version %s' % (version, self.VERSION))

    def jumpahead(self, n):
        if not n >= 0:
            raise ValueError('n must be >= 0')
        x, y, z = self._seed
        x = int(x * pow(171, n, 30269)) % 30269
        y = int(y * pow(172, n, 30307)) % 30307
        z = int(z * pow(170, n, 30323)) % 30323
        self._seed = (x, y, z)

    def __whseed(self, x = 0, y = 0, z = 0):
        if not type(x) == type(y) == type(z) == int:
            raise TypeError('seeds must be integers')
        if (0 <= x < 256 and 0) <= y < 256:
            raise 0 <= z < 256 or ValueError('seeds must be in range(0, 256)')
        if 0 == x == y == z:
            import time
            t = long(time.time() * 256)
            t = int(t & 16777215 ^ t >> 24)
            t, x = divmod(t, 256)
            t, y = divmod(t, 256)
            t, z = divmod(t, 256)
        self._seed = x or (1, y or 1, z or 1)
        self.gauss_next = None
        return

    def whseed(self, a = None):
        if a is None:
            self.__whseed()
            return
        a = hash(a)
        a, x = divmod(a, 256)
        a, y = divmod(a, 256)
        a, z = divmod(a, 256)
        x = (x + a) % 256 or 1
        y = (y + a) % 256 or 1
        z = (z + a) % 256 or 1
        self.__whseed(x, y, z)
        return


class SystemRandom(Random):
    __module__ = __name__

    def random(self):
        return (long(_hexlify(_urandom(7)), 16) >> 3) * RECIP_BPF

    def getrandbits(self, k):
        if k <= 0:
            raise ValueError('number of bits must be greater than zero')
        if k != int(k):
            raise TypeError('number of bits should be an integer')
        bytes = (k + 7) // 8
        x = long(_hexlify(_urandom(bytes)), 16)
        return x >> bytes * 8 - k

    def _stub(self, *args, **kwds):
        return None

    seed = jumpahead = _stub

    def _notimplemented(self, *args, **kwds):
        raise NotImplementedError('System entropy source does not have state.')

    getstate = setstate = _notimplemented


def _test_generator(n, func, args):
    import time
    print n, 'times', func.__name__
    total = 0.0
    sqsum = 0.0
    smallest = 10000000000.0
    largest = -10000000000.0
    t0 = time.time()
    for i in range(n):
        x = func(*args)
        total += x
        sqsum = sqsum + x * x
        smallest = min(x, smallest)
        largest = max(x, largest)

    t1 = time.time()
    print round(t1 - t0, 3), 'sec,',
    avg = total / n
    stddev = _sqrt(sqsum / n - avg * avg)
    print 'avg %g, stddev %g, min %g, max %g' % (avg,
     stddev,
     smallest,
     largest)


def _test(N = 2000):
    _test_generator(N, random, ())
    _test_generator(N, normalvariate, (0.0, 1.0))
    _test_generator(N, lognormvariate, (0.0, 1.0))
    _test_generator(N, vonmisesvariate, (0.0, 1.0))
    _test_generator(N, gammavariate, (0.01, 1.0))
    _test_generator(N, gammavariate, (0.1, 1.0))
    _test_generator(N, gammavariate, (0.1, 2.0))
    _test_generator(N, gammavariate, (0.5, 1.0))
    _test_generator(N, gammavariate, (0.9, 1.0))
    _test_generator(N, gammavariate, (1.0, 1.0))
    _test_generator(N, gammavariate, (2.0, 1.0))
    _test_generator(N, gammavariate, (20.0, 1.0))
    _test_generator(N, gammavariate, (200.0, 1.0))
    _test_generator(N, gauss, (0.0, 1.0))
    _test_generator(N, betavariate, (3.0, 3.0))


_inst = Random()
seed = _inst.seed
random = _inst.random
uniform = _inst.uniform
randint = _inst.randint
choice = _inst.choice
randrange = _inst.randrange
sample = _inst.sample
shuffle = _inst.shuffle
normalvariate = _inst.normalvariate
lognormvariate = _inst.lognormvariate
expovariate = _inst.expovariate
vonmisesvariate = _inst.vonmisesvariate
gammavariate = _inst.gammavariate
gauss = _inst.gauss
betavariate = _inst.betavariate
paretovariate = _inst.paretovariate
weibullvariate = _inst.weibullvariate
getstate = _inst.getstate
setstate = _inst.setstate
jumpahead = _inst.jumpahead
getrandbits = _inst.getrandbits
if __name__ == '__main__':
    _test()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\random.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:25 Pacific Daylight Time
