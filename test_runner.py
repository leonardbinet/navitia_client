# https://www.internalpointers.com/post/run-painless-test-suites-python-unittest

import unittest

# load package to initialize
import test
# import test modules
import test.test_client as test_client
import test.test_explore as test_explore

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_client))
suite.addTests(loader.loadTestsFromModule(test_explore))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
