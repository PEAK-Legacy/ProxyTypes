import unittest
from peak.util.proxies import *

class ProxyTestMixin:

    def checkInteger(self, v):
        p = self.proxied(v)
        self.assertEqual(p|010101, v|010101)
        self.assertEqual(p&010101, v&010101)
        self.assertEqual(p^010101, v^010101)
        self.assertEqual(~p, ~v)
        self.assertEqual(p<<3, v<<3)
        self.assertEqual(p>>2, v>>2)
        for f in hex, oct:
            self.assertEqual(f(p), f(v))
        self.checkNumeric(v)

    def checkNumeric(self, v):
        p = self.proxied(v)
        self.assertEqual(p*2, v*2)
        self.assertEqual(2*p, 2*v)
        self.assertEqual(2**p, 2**v)
        self.assertEqual(p**2, v**2)
        self.assertEqual(-p, -v)
        self.assertEqual(+p, +v)
        for f in abs, int, long, float, hash, complex:
            self.assertEqual(f(p), f(v))
        self.assertEqual(p<22, v<22)
        self.assertEqual(p>=10, v>=10)
        self.assertEqual(p>9.0, v>9.0)
        self.assertEqual(p<=9.25, v<=9.25)
        self.assertEqual(p==7, v==7)
        self.assertEqual(p!=18, v!=18)

        self.assertEqual(22<p, 22<v)
        self.assertEqual(10>=p, 10>=v)
        self.assertEqual(9.0>p, 9.0>v)
        self.assertEqual(9.25<=p, 9.25<=v)
        self.assertEqual(7==p, 7==v)
        self.assertEqual(18!=p, 18!=v)

        self.assertEqual(cmp(p,14), cmp(v,14))
        self.assertEqual(cmp(14,p), cmp(14,v))

        self.assertEqual(divmod(p,3), divmod(v,3))
        if v: self.assertEqual(divmod(3,p), divmod(3,v))
        self.checkBasics(v)

    def checkList(self, v):
        p = self.proxied(v)
        for i in range(len(v)):
            self.assertEqual(p[i], v[i])
            self.assertEqual(p[i:], v[i:])
            self.assertEqual(p[:i], v[:i])
            self.assertEqual(p[i::-1], v[i::-1])
        self.checkContainer(v)

        c = list(v)
        del p[::1]
        del c[::1]
        self.assertEqual(v, c)

        p[1:1] = [23]
        c[1:1] = [23]
        self.assertEqual(v, c)

    def checkContainer(self, v):
        p = self.proxied(v)
        self.assertEqual(list(p), list(v))
        self.assertEqual(list(iter(p)), list(iter(v)))
        self.assertEqual(len(p), len(v))
        self.assertEqual(42 in p, 42 in v)
        self.assertEqual(99 in p, 99 in v)
        self.checkBasics(v)

    def checkBasics(self, v):
        p = self.proxied(v)
        for f in bool, repr, str:
            self.assertEqual(f(p), f(v))



    def testNumbers(self):
        for i in range(20):
            self.checkInteger(i)

        f = -40
        while f<=20.0:
            self.checkNumeric(f)
            f += 2.25

    def testLists(self):
        from UserList import UserList
        for d in [1,2], [3,42,59], [99,23,55]:
            self.checkList(d)
            self.checkList(UserList(d))


class TestObjectProxy(ProxyTestMixin, unittest.TestCase):
    proxied = ObjectProxy

class TestCallbackProxy(ProxyTestMixin, unittest.TestCase):
    proxied = lambda self, v: CallbackProxy(lambda:v)

class TestLazyProxy(ProxyTestMixin, unittest.TestCase):
    proxied = lambda self, v: LazyProxy(lambda:v)

def additional_tests():
    import doctest
    return doctest.DocFileSuite(
        'README.txt', 'quirky-tests.txt', optionflags=doctest.ELLIPSIS,
    )











