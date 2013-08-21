exconsole
=========

Emergency/postmortem Python console

Installation from PyPI::

    pip install python-exconsole

DEB and RPM packages are available in Ajenti repositories: http://docs.ajenti.org/man/install/general.html

Quick start::

    import exconsole
    exconsole.register()

    do_dangerous_stuff()


Example of work::

    Activating emergency console
    ----------------------------
    Caused by:
    ZeroDivisionError
    integer division or modulo by zero

    Stack frames:
      [  0] example.py:17
              
      [  1] example.py:15
                  Tester().test()
      [  2] example.py:9
                      self.inner()
      [  3] example.py:6
                      self.divide(2, 0)
    > [  4] example.py:3
                      return a / b
    On frame 4
    Source:
               def divide(self, a, b):
        >>         return a / b

    Press Ctrl-D to leave console
    Type "_help()"" for built-in commands

    >>> print a,b
    2 0
    >>> _f(3)
    On frame 3
    Source:
               def inner(self):
        >>         self.divide(2, 0)

    >>> print self
    <__main__.Tester instance at 0x7f67c9a0e440>
