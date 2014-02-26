from twisted.trial import unittest, runner, reporter

from chat.test import test_parse_url
from chat.test import test_user
from chat.test import test_channel
# from chat.test import test_post
# from chat.test import test_protocol
from chat.test import test_email
from chat.test import test_stress
from chat.test import test_utils


if __name__ == '__main__':
  results = reporter.TreeReporter()
  suite = unittest.TestSuite()

  tests = [
    # test_email,
    # test_protocol,
    #test_post,
    test_parse_url,
    test_stress,
    test_utils,
    test_channel,
    test_user
  ]

  for alias in tests:
    alias = runner.TestLoader().loadModule(alias)
    suite.addTests(alias)

  suite.run(results)
  results.done()