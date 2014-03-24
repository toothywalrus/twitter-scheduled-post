"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import nose.tools as nt


class Foo:

    def exist(self):
        return True

    def get(self):
        raise IOError('access denied')

    def calc(self, v):
        return 2 * v


class TestFoo:

    def setUp(self):
        self.multiplier = 2

    def teardown(self):
        pass

    def test_exist(self):
        f = Foo()
        nt.assert_true(f.exist())

    def test_get(self):
        f = Foo()
        nt.assert_raises(IOError, f.get)

    def test_calc(self):
        f = Foo()
        assert f.calc(self.multiplier) != 5
