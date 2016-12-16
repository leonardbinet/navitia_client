# https://www.internalpointers.com/post/run-painless-test-suites-python-unittest

import unittest

# load package to initialize
import test
# import test modules
from test import test_client, test_explore, test_inverted_geocoding, test_journeys, test_route_schedules

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_client))
suite.addTests(loader.loadTestsFromModule(test_explore))
suite.addTests(loader.loadTestsFromModule(test_inverted_geocoding))
suite.addTests(loader.loadTestsFromModule(test_journeys))
suite.addTests(loader.loadTestsFromModule(test_route_schedules))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
