class Tester:
    def divide(self, a, b):
        return a / b

    def inner(self):
        self.divide(2, 0)

    def test(self):
        self.inner()

import exconsole
exconsole.register()

def fun():
    Tester().test()

fun()
