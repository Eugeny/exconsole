class Tester:
    def divide(self, a, b):
        return a / b

    def inner(self):
        self.divide(2, 0)

    def test(self):
        self.inner()

import exconsole

def testcmd(*args, **kwargs):
    print 'Test!'

exconsole.register(commands=[('_t', 'Test', testcmd)])

def fun():
    Tester().test()

fun()
